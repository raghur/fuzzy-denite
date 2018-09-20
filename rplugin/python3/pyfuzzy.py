import sys
import functools
import heapq

sep = '/\_.'


def scorer(x, key):
    candidate = key(x[0])
    # print("item is", candidate)
    # how close to the end of string as pct
    position_boost = 100 * (x[1][0]/len(candidate))
    # absolute value of how close it is to end
    end_boost = 100 - x[3]

    # how closely are matches clustered
    cluster_boost = 100 * (1 - x[2]/len(candidate)) * 2

    # boost for matches after separators
    # weighted by length of query
    sep_boost = 100 * x[4]/len(x[1]) * 0.25
    return position_boost + end_boost + cluster_boost + sep_boost


def scoreMatches(query, candidates, limit, key=None):
    def idfn(x):
        return x
    key = idfn if not key else key
    matches = fuzzyMatches(query, candidates, limit * 5, key)
    return heapq.nlargest(limit, matches, key=lambda x: scorer(x, key))


def isMatch(query, candidate, left, right):
    matchPos = []
    d = "r"
    sepScore = 0
    clusterScore = 0
    for i, c in enumerate(query):
        if d == "r":
            pos = candidate.rfind(c, left, right - i)
        else:
            pos = candidate.find(c, left, right)
        if pos == -1:
            return (False, matchPos)
        else:
            sepScore = sepScore + 1 if candidate[pos -1] in sep else sepScore
            matchPos.append(pos)
            if len(matchPos) > 1:
                clusterScore = clusterScore + matchPos[-1] - matchPos[-2] - 1
            left = pos + 1
            if d == "r":
                d = "l"

    return (True, matchPos, clusterScore, len(candidate) - matchPos[0], sepScore)


def fuzzyMatches(query, candidates, limit, key=None):
    """Find fuzzy matches among given candidates

    :query: TODO
    :candidates: TODO
    :limit: TODO
    :returns: TODO

    """
    findFirstN = True
    count = 0
    for x in candidates:
        s = key(x)
        l, r = 0, len(s)
        didMatch = False
        positions = []
        while not didMatch:
            didMatch, positions, *rest = isMatch(query, s, l, r)
            if not positions:
                break
            r = positions[0]
        if didMatch:
            count = count + 1
            yield (x, positions, *rest)
            if findFirstN and count == limit:
                return


def usage():
    """TODO: Docstring for usage.
    :returns: TODO

    """
    print("usage")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit(0)

    file = "neomru_file"
    query = sys.argv[1]
    if len(sys.argv) == 3:
        file = sys.argv[1]
        query = sys.argv[2]

    with open(file) as fh:
        lines = (line.strip() for line in fh.readlines())
        for x in scoreMatches(query, lines, 10):
            print(x)

