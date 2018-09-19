import sys
import functools
import heapq

sep = '/\_.'


def scorer(x):
    # how close to the end of string as pct
    position_boost = 100 * x[1][-1]/len(x[0])

    # absolute value of how close it is to end
    end_boost = 100 - x[3]

    # how closely are matches clustered
    cluster_boost = 100 * (1 - x[2]/len(x[0]))

    # boost for matches after separators
    # weighted by length of query
    sep_boost = 100 * x[4]/len(x[1]) * 0.5
    return position_boost + end_boost + cluster_boost + sep_boost


def scoreMatches(matches, limit):
    return heapq.nlargest(limit, matches, key=scorer)


def isMatch(query, candidate, left, right):
    matchPos = []
    d = "r"
    for c in query:
        if d == "r":
            pos =  candidate.rfind(c, left, right)
        else:
            pos = candidate.find(c, left, right)
        if pos == -1:
            return (False, matchPos)
        else:
            matchPos.append(pos)
            left = pos + 1
            if d == "r":
                d = "l"

    return (True, matchPos)


def fuzzyMatches(query, candidates, limit):
    """Find fuzzy matches among given candidates

    :query: TODO
    :candidates: TODO
    :limit: TODO
    :returns: TODO

    """
    findFirstN = False
    count = 0
    for x in candidates:
        l,r = 0, len(x)
        didMatch = False
        positions = []
        while not didMatch:
            didMatch, positions = isMatch(query, x, l, r)
            if not positions:
                break
            r = positions[0]
        if didMatch:
            clusterScore = 0
            for i, p in enumerate(positions):
                if i > 0:
                    clusterScore = positions[i] - positions[i-1] - 1
            sepscore = functools.reduce(lambda x, y: x+y, 
                                        map(lambda p: 1 if x[p - 1] in sep else
                                            0, positions))
            count = count + 1
            yield (x, positions, clusterScore, len(x) - positions[0], sepscore)
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
        for x in scoreMatches(fuzzyMatches(query, lines, 10), 10):
            print(x)

