package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"

	lru "github.com/hashicorp/golang-lru"
	"github.com/hydrogen18/stalecucumber"
	"github.com/sahilm/fuzzy"
	"github.com/schollz/closestmatch"
	log "github.com/sirupsen/logrus"
)

var contexts *lru.ARCCache

func matchFuzzy(pattern string, context interface{}, max int) *[]string {
	data := context.(*[]string)
	matches := fuzzy.Find(pattern, *data)
	if max == 0 {
		max = len(matches)
	}
	arr := make([]string, max)
	for i, m := range matches {
		if i == len(arr) {
			break
		}
		arr[i] = m.Str
	}
	return &arr
}

func createContext(cid, algo string, data *[]string) {
	switch algo {
	case "fuzzy":
		contexts.Add(cid, &data)
	case "closestmatch":
		log.Info("Creating closestmatch context ", cid)
		bagSizes := []int{2, 3, 4, 5, 6, 7}
		cm := closestmatch.New(*data, bagSizes)
		contexts.Add(cid, cm)
	}
}
func matchClosestMatch(pattern string, context interface{}, max int) *[]string {
	cm := context.(*closestmatch.ClosestMatch)
	matches := cm.ClosestN(pattern, max)
	return &matches
}
func findMatchesFromContext(cid, pattern, algo string, max int, writer io.Writer) {
	log.Infof("Searching for %v in context %v", pattern, cid)
	var matches *[]string
	ctx, _ := contexts.Get(cid)
	switch algo {
	case "fuzzy":
		matches = matchFuzzy(pattern, ctx, max)
	case "closestmatch":
		matches = matchClosestMatch(pattern, ctx, max)
	}

	log.Debugf("number of matches: %v", len(*matches))
	log.Infof("%v matches for %v. Will return max: %v results", len(*matches), pattern, max)

	p := stalecucumber.NewPickler(writer)
	p.Pickle(*matches)
}

func findMatches(reader io.Reader, pattern string, max int, writer io.Writer) {
	log.Debugf("Searching for %v", pattern)
	files := make([]string, 0)
	err := stalecucumber.UnpackInto(&files).From(stalecucumber.Unpickle(reader))
	if err != nil {
		log.Errorf("Could not read pickled stream %v", err)
	}
	log.Debugf("length of array %v", len(files))
	matches := fuzzy.Find(pattern, files)
	if max == 0 {
		max = len(matches)
	}
	arr := make([]string, max)
	for i, m := range matches {
		if i == len(arr) {
			break
		}
		arr[i] = m.Str
	}
	log.Debugf("number of matches: %v", len(matches))
	log.Infof("Got %v items. %v matches for %v. Will return max: %v results", len(files), len(matches), pattern, max)

	p := stalecucumber.NewPickler(writer)
	p.Pickle(arr)
}

func main() {

	http.HandleFunc("/search", func(w http.ResponseWriter, r *http.Request) {
		file, _, fileerr := r.FormFile("data")
		cid := r.Form.Get("cid")
		if cid == "" {
			log.Errorf("Called /search without required param cid")
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte("You must pass a cid param"))
			return
		}
		ok := contexts.Contains(cid)
		if !ok && fileerr != nil {
			log.Errorf("/search: Context %v does not exist and no data passed", cid)
			w.WriteHeader(http.StatusBadRequest)
			w.Write([]byte(fmt.Sprintf("You did not pass data for context id %v", cid)))
			return
		}
		algo := r.Form.Get("algo")
		if algo != "closestmatch" || algo != "fuzzy" {
			algo = "closestmatch"
		}
		if !ok {
			data := make([]string, 0)
			err := stalecucumber.UnpackInto(&data).From(stalecucumber.Unpickle(file))
			if err != nil {
				log.Errorf("Could not read pickled stream %v", err)
				w.WriteHeader(http.StatusInternalServerError)
			}
			createContext(cid, algo, &data)
			log.Infof("Created new context %v of size %v", cid, len(data))
		}
		max := r.Form.Get("max")
		maxi, err := strconv.ParseInt(max, 10, 0)
		if err != nil {
			maxi = 0
		}
		findMatchesFromContext(cid, r.Form.Get("pattern"), algo, int(maxi), w)
	})

	// http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
	// 	for k, v := range r.Header {
	// 		log.Debugf("Header %v: %v", k, v)
	// 	}
	// 	file, _, _ := r.FormFile("data")
	// 	max := r.Form.Get("max")
	// 	maxi, err := strconv.ParseInt(max, 10, 0)
	// 	if err != nil {
	// 		maxi = 0
	// 	}
	// 	findMatches(file, r.Form.Get("pattern"), int(maxi), w)
	// })
	contexts, _ = lru.NewARC(20)
	log.Info("starting")
	http.ListenAndServe(":80", nil)
}
