import nimpy
import strutils
import binaryheap
import logging

# let L = newConsoleLogger(levelThreshold = logging.Level.lvlDebug)
let L = newConsoleLogger(levelThreshold = logging.Level.lvlError)
addHandler(L)

const sep:string = "-/\\_. "

type
    Match = object
        found:bool
        positions: seq[int]
        sepScore, clusterScore, camelCaseScore: int

proc scorer(x: Match, candidate:string, ispath:bool=true): int =
    let lqry = len(x.positions)
    let lcan = len(candidate)

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

proc isMatch(query, candidate: string): Match =

    proc walkString(q, c: string, left, right: int): Match =
        debug "Call ", query, left, right
        if left > right or right == 0:
            result.found = false
            return
        var orig = c
        var candidate = strutils.toLowerAscii(c)
        var query = strutils.toLowerAscii(q)
        var first = true
        var pos:int = -1
        var l = left
        var r = right
        result.positions = newSeq[int](len(q))
        for i, c in query:
            debug "Looking", i, c, left, right
            if first:
                pos = strutils.rfind(candidate, c, r)
            else:
                pos = strutils.find(candidate, c, l)
            debug "Result", i, pos, c
            if pos == -1:
                result.found = false
                if first:
                    # if the first char was not found anywhere we're done
                    return 
                else:
                    # otherwise, find the non matching char to the left of the
                    # first char pos. Next search on has to be the left of this
                    # position
                    if result.positions[0] == 0:
                        result.positions = @[]
                        return
                    var posLeft = strutils.rfind(candidate, c, result.positions[0] - 1)
                    debug "posLeft ", c, result.positions[0], posLeft
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
                result.positions[i] = pos
                if i > 0:
                    result.clusterScore = result.clusterScore + result.positions[i] - result.positions[i - 1] - 1
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
            result.found = false
            break  # all done too - first char didn't match

        # resume search - start looking left from this position onwards
        r = result.positions[0]
        if r == 0:
            result.found = false
            break
    return

iterator fuzzyMatches(query:string, candidates: openarray[string], limit: int, ispath: bool = true): tuple[i:int, r:int] =
    let findFirstN = true
    var count = 0
    var heap = newHeap[tuple[i:int, r:int]]() do (a, b: tuple[i:int, r:int]) -> int:
        b.r - a.r
    # var heap = newHeapQueue[Match[T]]()
    for i, x in candidates:
        debug "processing: ", x
        var res = isMatch(query, x)
        if res.found:
            count = count + 1
            debug "ADDED: ", x
            let rank = scorer(res, x, ispath)
            heap.push((i, rank))
            if findFirstN and count == limit * 5:
                break
    var c = 0
    while c < limit and heap.size > 0:
        let item =  heap.pop
        yield item
        c = c + 1

proc scoreMatchesStr(query: string, candidates: openarray[string], limit: int, ispath:bool=true): seq[tuple[i:int, r:int]] {.exportpy.} =
    result = newSeq[tuple[i:int, r:int]](limit)
    var idx = 0
    for m in fuzzyMatches(query, candidates, limit, ispath):
        result[idx] = m
        idx.inc
    result.setlen(idx)
    return
