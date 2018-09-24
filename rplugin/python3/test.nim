import nimpy
import strutils

const sep:string = "-/\\_. "
proc greet(name: string): string {.exportpy.} =
    return "Hello, " & name & "!"



proc arr(items: seq[string]): seq[string] {.exportpy.} =
    var r = newSeq[string](len(items))
    for i, x in items:
        r[i] = x
    return r


type
    MyObj = object
        a, b: int
        c: string

    MyRefObj = ref MyObj

type
    Candidate = object
        abbr, source_name, word: string
        source_index: int
type
    Match = object
        found:bool
        candidate: string
        positions: seq[int]
        sepScore, clusterScore, camelCaseScore: int



proc getMyObj(): MyObj {.exportpy.} =
    result.a = 5
    result.c = "hello"

proc isMatch(query, candidate: string): Match =

    proc walkString(q, c: string, left, right: int): Match =
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
                    return
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

iterator fuzzyMatches(query:string, candidates: openarray[Candidate], limit: int): Candidate = 
    var findFirstN = true
    var count = 0
    for x in candidates:
        var s = x.word
        var res = isMatch(query, s)
        if res.found:
            count = count + 1
            yield x
            if findFirstN and count == limit:
                break


proc scoreMatches(query: string, candidates: openarray[Candidate], limit: int): seq[Candidate] {.exportpy.} =
    result = @[]
    for m in fuzzyMatches(query, candidates, limit * 5):
        result.add(m)
    return
    # return iterator

