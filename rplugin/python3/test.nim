import nimpy
import strutils
import binaryheap

const sep:string = "-/\\_. "

type
    Candidate = object
        abbr, source_name, word: string
        source_index: int
type
    Match[T] = object
        found:bool
        candidate: T
        positions: seq[int]
        sepScore, clusterScore, camelCaseScore: int


proc scorer[T](x: Match[T], fn: proc(x:T):string, ispath:bool=true): int =
    let lqry = len(x.positions)
    let lcan = len(fn(x.candidate))

    var position_boost = 0
    var end_boost = 0
    if ispath:
        # print("item is", candidate)
        # how close to the end of string as pct
        position_boost = 100 * (x.positions[0] div lcan)
        # absolute value of how close it is to end
        end_boost = (100 - (lcan - x.positions[0])) * 2

    # how closely are matches clustered
    var cluster_boost = 100 * (1 - x.clusterScore div lcan) * 4

    # boost for matches after separators
    # weighted by length of query
    var sep_boost = (100 * x.sepScore div lqry) * 75 div 100

    # boost for camelCase matches
    # weighted by lenght of query
    var camel_boost = 100 * x.camelCaseScore div lqry

    return position_boost + end_boost + cluster_boost + sep_boost + camel_boost

proc isMatch[T](query, candidate: string): Match[T] =

    proc walkString(q, c: string, left, right: int): Match[T] =
        # print("Call ", query, left, right)
        var orig = c
        var candidate = strutils.toLowerAscii(c)
        var query = strutils.toLowerAscii(q)
        var first = true
        var pos:int = -1
        var l = left
        var r = right
        result.positions = @[]
        for i, c in query:
            # print ("Looking", i, c, left, right)
            if first:
                pos = strutils.rfind(candidate, c, r)
            else:
                pos = strutils.find(candidate, c, l)
            # print("Result", i, pos, c)
            if pos == -1:
                result.found = false
                if first:
                    # if the first char was not found anywhere we're done
                    return 
                else:
                    # otherwise, find the non matching char to the left of the
                    # first char pos. Next search on has to be the left of this
                    # position
                    var posLeft = strutils.rfind(candidate, c, result.positions[0])
                    if posLeft != -1:
                        result.positions = @[posLeft]
                    else:
                        result.positions = @[]
                    return
            else:
                if pos == 0:
                    result.sepScore = result.sepScore + 1
                    result.camelCaseScore = result.camelCaseScore + 1
                else:
                    var prevChar = orig[pos - 1]
                    if prevChar in sep:
                        result.sepScore = result.sepScore + 1
                    if ord(orig[pos]) < 97 and ord(prevChar) >= 97:
                        result.camelCaseScore = result.camelCaseScore + 1
                result.positions.add(pos)
                if len(result.positions) > 1:
                    var last = len(result.positions) - 1
                    result.clusterScore = result.clusterScore + result.positions[last] - result.positions[last - 1] - 1
                l = pos + 1
                first = false
        result.found = true
        return

    var didMatch = false
    var l = 0
    var r = len(candidate)
    while not didMatch:
        result = walkString(query, candidate, l, r)
        if result.found:
            break  # all done
        if len(result.positions) == 0:
            break  # all done too - first char didn't match

        # resume search - start looking left from this position onwards
        r = result.positions[0]
    return

iterator fuzzyMatches[T](query:string, candidates: openarray[T], limit: int, fn: proc(c: T):string, ispath: bool = true): tuple[c:T, s:int] =
    var findFirstN = true
    var count = 0
    var heap = newHeap[tuple[c:T, s:int]]() do (a, b: tuple[c:T, s:int]) -> int:
        b.s - a.s
    for x in candidates:
        var s = fn(x)
        # echo "processing: ", s
        var res = isMatch[T](query, s)
        if res.found:
            res.candidate = x
            count = count + 1
            # echo s, "added to heap"
            heap.push((x, scorer[T](res, fn, ispath)))
            if findFirstN and count == limit * 5:
                break
    var c = 0
    while heap.size > 0 and c < limit:
        var x = heap.pop()
        yield x
        c = c + 1


proc scoreMatches(query: string, candidates: openarray[Candidate], limit: int, ispath: bool=true): seq[tuple[c:Candidate, s:int]] {.exportpy.} =
    proc getWord(x: Candidate): string = return x.word
    result = @[]
    for m in fuzzyMatches[Candidate](query, candidates, limit, getWord, ispath):
        result.add(m)
    return

proc scoreMatchesStr(query: string, candidates: openarray[string], limit: int, ispath:bool=true): seq[tuple[c:string, s:int]] {.exportpy.} =
    proc idfn(x: string):string = return x
    result = @[]
    # echo candidates
    for m in fuzzyMatches[string](query, candidates, limit, idfn, ispath):
        result.add(m)
    return
    # return iterator
