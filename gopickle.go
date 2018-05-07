package main

import (
	"github.com/hydrogen18/stalecucumber"
	"github.com/sahilm/fuzzy"
	log "github.com/sirupsen/logrus"
	"io"
	"net/http"
)

func findMatches(reader io.Reader, pattern string, writer io.Writer) {
	log.Infof("Searching for %v", pattern)
	files := make([]string, 0)
	err := stalecucumber.UnpackInto(&files).From(stalecucumber.Unpickle(reader))
	if err != nil {
		log.Errorf("Could not read pickled stream %v", err)
	}
	log.Infof("length of array %v", len(files))
	matches := fuzzy.Find(pattern, files)
	log.Infof("number of matches: %v", len(matches))
	p := stalecucumber.NewPickler(writer)
	p.Pickle(matches)
}

func main() {

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		for k, v := range r.Header {
			log.Infof("Header %v: %v", k, v)
		}
		file, _, _ := r.FormFile("data")
		findMatches(file, r.Form.Get("pattern"), w)
	})
	log.Info("starting")
	http.ListenAndServe(":80", nil)
}
