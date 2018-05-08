package lib

import (
	"fmt"
	"io"
	"net/http"
	"strconv"

	lru "github.com/hashicorp/golang-lru"
	"github.com/hydrogen18/stalecucumber"
	"github.com/sahilm/fuzzy"
	log "github.com/sirupsen/logrus"
)

var contexts *lru.ARCCache

func CreateServer(cacheSize int) {
	contexts, _ = lru.NewARC(cacheSize)
	http.HandleFunc("/search", search)
}

func search(w http.ResponseWriter, r *http.Request) {
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

	if !ok {
		data := make([]string, 0)
		err := stalecucumber.UnpackInto(&data).From(stalecucumber.Unpickle(file))
		if err != nil {
			log.Errorf("Could not read pickled stream %v", err)
			w.WriteHeader(http.StatusInternalServerError)
		}
		contexts.Add(cid, data)
		log.Infof("Created new context %v of size %v", cid, len(data))
	}
	max := r.Form.Get("max")
	maxi, err := strconv.ParseInt(max, 10, 0)
	if err != nil {
		maxi = 0
	}
	findMatchesFromContext(cid, r.Form.Get("pattern"), int(maxi), w)
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}
func findMatchesFromContext(cid, pattern string, max int, writer io.Writer) {
	log.Infof("Searching for %v in context %v", pattern, cid)
	v, _ := contexts.Get(cid)
	data := v.([]string)

	matches := fuzzy.Find(pattern, data)
	if max == 0 {
		max = len(matches)
	}

	max = min(len(matches), max)
	arr := make([]string, max)
	for i, m := range matches {
		if i == len(arr) {
			break
		}
		arr[i] = m.Str
	}
	log.Debugf("number of matches: %v", len(matches))
	log.Infof("Got %v items. %v matches for %v. Will return max: %v results", len(data), len(matches), pattern, max)

	p := stalecucumber.NewPickler(writer)
	p.Pickle(arr)
}
