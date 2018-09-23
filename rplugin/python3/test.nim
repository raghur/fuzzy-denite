import nimpy

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

proc getMyObj(): MyObj {.exportpy.} =
    result.a = 5
    result.c = "hello"

proc scoreMatches(items: seq[Candidate]): tuple[c:Candidate, l:int] {.exportpy.} =
    var c:int = 0
    for x in items:
        c = c + len(x.word)
    return (c:items[0], l:c)
