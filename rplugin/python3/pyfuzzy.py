import sys
import functools
import heapq

sep = '/\_.'


def scorer(x):
    # how close to the end of string as pct
    position_boost = 100 * (x[1][-1]/len(x[0]))
    # absolute value of how close it is to end
    end_boost = 100 - x[3]

    # how closely are matches clustered
    cluster_boost = 100 * (1 - x[2]/len(x[0])) * 2

    # boost for matches after separators
    # weighted by length of query
    sep_boost = 100 * x[4]/len(x[1]) * 0.25
    return position_boost + end_boost + cluster_boost + sep_boost


def scoreMatches(matches, limit):
    return heapq.nlargest(limit, matches, key=scorer)


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


def fuzzyMatches(query, candidates, limit):
    """Find fuzzy matches among given candidates

    :query: TODO
    :candidates: TODO
    :limit: TODO
    :returns: TODO

    """
    findFirstN = True
    count = 0
    for x in candidates:
        l, r = 0, len(x)
        didMatch = False
        positions = []
        while not didMatch:
            didMatch, positions, *rest = isMatch(query, x, l, r)
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
        for x in scoreMatches(fuzzyMatches(query, lines, 50), 10):
            print(x)

