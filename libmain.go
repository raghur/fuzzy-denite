// +build lib

package main

import "C"
import (
	"fmt"

	"github.com/sahilm/fuzzy"
)

func main() {}

//export FindMatches
func FindMatches(data []*C.char, pattern string, max int, results []*C.char) int {
	godata := make([]string, len(data))
	for i, v := range data {
		godata[i] = C.GoString(v)
	}
	matches := fuzzy.Find(pattern, godata)
	if max == 0 {
		max = len(matches)
	}

	max = min(len(matches), max)
	// log.Debugf("number of matches: %v", len(matches))
	// log.Infof("[%v] Size=%v, qry=%v, matches=%v, max=%v", cid, len(data), pattern, len(matches), max)
	for i, m := range matches[:max] {
		results[i] = C.CString(m.Str)
		// log.Debug(m.Str)
	}
	return max

}

//export Bar
func Bar(data string) *C.char {
	return C.CString(data + "howdy world!")
}

//export Foo
func Foo(data []*C.char, matches []*C.char) int {
	// ret := make([]string, len(data))
	// for i, v := range data {
	// 	fmt.Println(i, v)
	// 	ret[i] = v + " world"
	// }
	// return ret
	fmt.Println(len(data))
	for i, v := range data {
		fmt.Println(i, C.GoString(v))
	}
	s := []string{"Hello", "WOrld"}
	for i, v := range s {
		matches[i] = C.CString(C.GoString(data[i]) + " " + v)
	}
	return len(s)
}
func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}
