package lib

import (
	"fmt"
	"net/http"
	"strconv"

	lru "github.com/hashicorp/golang-lru"
	"github.com/hydrogen18/stalecucumber"
	"github.com/sahilm/fuzzy"
	log "github.com/sirupsen/logrus"
	context "golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

var contexts *lru.ARCCache

type server struct{}

func CreateGRPCServer(cacheSize int) *grpc.Server {
	contexts, _ = lru.NewARC(cacheSize)
	s := grpc.NewServer()
	RegisterFuzzyServer(s, &server{})
	reflection.Register(s)
	return s
}
func CreateServer(cacheSize int) {
	contexts, _ = lru.NewARC(cacheSize)
	http.HandleFunc("/search", search)
}
func (s *server) Match(ctx context.Context, req *FuzzyRequest) (*FuzzyReply, error) {
	cid := req.GetCid()
	if cid == "" {
		log.Errorf("Cid not supplied.")
		return &FuzzyReply{
			Code:  400,
			Msg:   "Cid not supplied.",
			Match: []string{},
		}, nil
	}
	ok := contexts.Contains(cid)
	if !ok {
		data := req.GetData()
		if len(data) == 0 {
			log.Errorf("Context does not exist and data not supplied.")
			return &FuzzyReply{
				Code:  400,
				Msg:   "Context does not exist and data not supplied.",
				Match: []string{},
			}, nil
		}
		contexts.Add(cid, data)
	}
	matches := findMatchesFromContext(cid, req.GetQry(), int(req.GetMax()))
	return &FuzzyReply{
		Code:  200,
		Msg:   "Ok",
		Match: *matches,
	}, nil
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
	matches := findMatchesFromContext(cid, r.Form.Get("pattern"), int(maxi))
	p := stalecucumber.NewPickler(w)
	p.Pickle(matches)
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}
func findMatchesFromContext(cid, pattern string, max int) *[]string {
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
	log.Infof("[%v] Size=%v, qry=%v, matches=%v, max=%v", cid, len(data), pattern, len(matches), max)
	return &arr

}
