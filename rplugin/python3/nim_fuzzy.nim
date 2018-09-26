import nimpy
import strutils
import binaryheap
import logging
import strformat

let L = newConsoleLogger(levelThreshold = logging.Level.lvlDebug)
addHandler(L)
const MAXCHARS = 10
const MAXCHARCOUNT = 10

const sep:string = "-/\\_. "

template l(fmt: string) =
    when not defined(release):
        debug(&fmt)
type
    Match = object
        found:bool
        positions: seq[int]
        sepScore, clusterScore, camelCaseScore: int
    MatchIndex = array[MAXCHARS, array[0..MAXCHARCOUNT, int]]

# forward declaration
proc scorer(x: Match, candidate:string, ispath:bool=true): int {.inline.}

proc assignScore(s: string, m: var Match) =
    let l = m.positions.len
    # min possible for consecutive matches like [51, 52, 53, 54]
    # = 51 * 4 + (4*3/2)
    # = 210
    m.clusterScore = -1 * (m.positions[0] * l + l * (l-1) div 2)
    for i,v in m.positions:
        if v == 0:
            m.sepScore.inc
            m.clusterScore.inc
        else:
            let
                prevChar = s[v-1]
                ch = s[v]
            if prevChar in sep:
                m.sepScore.inc
            if prevChar.isLowerAscii and ch.isUpperAscii:
                m.camelCaseScore.inc
        m.clusterScore.inc(v)

proc rfirst1(a: openarray[int], predicate: proc(x: int): bool, last:int = -1): tuple[f:bool, v:int] =
    #[
    Find first item matching predicate in a(last .. 0)
    ]#
    var s = last
    if s == -1: s = a.high
    for i in countdown(s, 0):
        if predicate(a[i]):
            return (true, a[i])
    return (false, -1)

proc greaterThan(x : int): (proc(x:int):bool) = 
    return proc(y:int):bool = return y > x

proc checkFullMatch(indexArr: MatchIndex, lq: string, pos: int, m: var Match) =
    var start = pos
    m.positions[0] = start
    l "Checking for entire string match starting from {pos}"
    m.found = true
    for k in 1..lq.high:
        let arrIdx = lq.find(lq[k])
        l "looking for {lq[k]} in {indexArr[arrIdx]}, greater than {start}"
        let (found, v) = rfirst1(indexArr[arrIdx], greaterThan(start), indexArr[arrIdx][MAXCHARCOUNT] - 1)
        if found:
            l "found at: {v}"
            start = v
            m.positions[k] = v
        else:
            m.found = false
            break

proc matcher(q, s: string):Match =
    var indexArr: MatchIndex
    let
        lq = q.toLowerAscii()
        ls = s.toLowerAscii()

    result.found = false
    result.positions = newSeq[int](len(q))
    l "looking for {q} in {s}"
    for i in countdown(ls.high, 0):
        let c = ls[i]
        let pos = lq.find(c)
        if pos != -1:
            let nextPos = indexArr[pos][MAXCHARCOUNT]
            indexArr[pos][nextPos] = i
            indexArr[pos][MAXCHARS].inc
            l "found {c} at {i}, indexArr[{pos}][{nextPos}]={indexArr[pos][nextPos]}"
            if pos == 0:
                # first char was found - so see if we found the entire string
                # after index i
                checkFullMatch(indexArr, lq, i, result)
                if result.found:
                    assignScore(s, result)
                    l "match: {result}"
                    return
    l "no match: {result}"
    return result

iterator fuzzyMatches01(q: string, candidates: openarray[string], limit: int, ispath:bool = true):tuple[i:int, r:int] =
    let findFirstN = true
    var count = 0
    var heap = newHeap[tuple[i:int, r:int]]() do (a, b: tuple[i:int, r:int]) -> int:
        b.r - a.r
    for i, s in candidates:
        let m = matcher(q, s)
        if m.found:
            let rank = scorer(m, s, ispath)
            heap.push((i, rank))
            count.inc
            if findFirstN and count == limit * 5:
                break
    count = 0
    while count < limit and heap.size > 0:
        yield  heap.pop
        count.inc

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

proc walkString(q, c: string, left, right: int, m: var Match)=
    l "Call {q} {left} {right}"
    if left > right or right == 0:
        m.found = false
        return
    var orig = c
    var candidate = strutils.toLowerAscii(c)
    var query = strutils.toLowerAscii(q)
    var first = true
    var pos:int = -1
    var l = left
    var r = right
    for i, c in query:
        l "Looking: {i}, {c}, {l}, {r}"
        if first:
            pos = strutils.rfind(candidate, c, r)
        else:
            pos = strutils.find(candidate, c, l)
        l "Result: {i}, {pos}, {c}"
        if pos == -1:
            m.found = false
            if first:
                # if the first char was not found anywhere we're done
                m.positions[0] = 0
                return 
            else:
                # otherwise, find the non matching char to the left of the
                # first char pos. Next search on has to be the left of this
                # position
                let np = m.positions[0] - 1
                if np < 0:
                    # we've run out - clearly, no match possible
                    m.positions[0] = 0
                    return
                var posLeft = strutils.rfind(candidate, c, np)
                l "posLeft:  {c}, {np}, {posLeft}"
                m.positions[0] = posLeft
                return
        else:
            if pos == 0:
                m.sepScore.inc
                m.camelCaseScore.inc
            else:
                var prevChar = orig[pos - 1]
                if prevChar in sep:
                    m.sepScore.inc
                if ord(orig[pos]) < 97 and ord(prevChar) >= 97:
                    m.camelCaseScore.inc
            m.positions[i] = pos
            if i == 0:
                let qlen = q.len
                m.clusterScore = -1 * ((pos * qlen) + (qlen * (qlen-1) div 2))
            m.clusterScore.inc(pos)
            l = pos + 1
            first = false
    m.found = true
    return

proc isMatch(query, candidate: string, m: var Match) =
    var didMatch = false
    var r = len(candidate)
    while not didMatch:
        walkString(query, candidate, 0, r, m)
        if m.found:
            break  # all done
        # resume search - start looking left from this position onwards
        r = m.positions[0]
        if r <= 0:
            m.found = false
            break
    return

proc resetMatch(m: var Match, l:int) = 
    m.found = false
    for j in 0 ..< l:
        m.positions[j] = 0
    m.clusterScore =0
    m.sepScore = 0
    m.camelCaseScore = 0

iterator fuzzyMatches(query:string, candidates: openarray[string], limit: int, ispath: bool = true): tuple[i:int, r:int] =
    let findFirstN = true
    var count = 0
    var mtch:Match
    mtch.positions = newSeq[int](query.len)
    var heap = newHeap[tuple[i:int, r:int]]() do (a, b: tuple[i:int, r:int]) -> int:
        b.r - a.r
    for i, x in candidates:
        l "processing:  {x}"
        resetMatch(mtch, query.len)
        isMatch(query, x, mtch)
        if mtch.found:
            count = count + 1
            l "ADDED: {x}"
            let rank = scorer(mtch, x, ispath)
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
    # for m in fuzzyMatches01(query, candidates, limit, ispath):
    for m in fuzzyMatches(query, candidates, limit, ispath):
        result[idx] = m
        idx.inc
    result.setlen(idx)
    return
