package main

import (
	"io"
	"os"

	log "github.com/sirupsen/logrus"

	"net/http"

	"github.com/hydrogen18/stalecucumber"
	"github.com/sahilm/fuzzy"
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
	log.Info("startign")
	http.ListenAndServe(":80", nil)
	files := make([]string, 0)
	reader, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal("could not read file %v, %e", os.Args[1], err)
	}
	err = stalecucumber.UnpackInto(&files).From(stalecucumber.Unpickle(reader))
	log.Infof("length of array %v", len(files))

	matches := fuzzy.Find("grrf", files)
	log.Infof("number of matches: %v", len(matches))
	of, _ := os.Create(os.Args[2])
	p := stalecucumber.NewPickler(of)
	p.Pickle(matches)
	defer func() {
		of.Close()
	}()
}
