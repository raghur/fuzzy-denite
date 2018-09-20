import sys
import functools
import heapq

sep = '/\_.'


def idfn(x):
    return x


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
    key = idfn if not key else key
    matches = fuzzyMatches(query, candidates, limit * 5, key)
    return heapq.nlargest(limit, matches, key=lambda x: scorer(x, key))


def isMatch(query, candidate):
    def walkString(query, candidate, left, right):
        # print("Call ", query, left, right)
        matchPos = []
        first = True
        sepScore = 0
        clusterScore = 0
        for i, c in enumerate(query):
            # print ("Looking", i, c, left, right)
            if first:
                pos = candidate.rfind(c, left, right)
            else:
                pos = candidate.find(c, left)
            # print("Result", i, pos, c)
            if pos == -1:
                if first:
                    # if the first char was not found anywhere we're done
                    return (False, [])
                else:
                    # otherwise, find the non matching char to the left of the
                    # first char pos. Next search on has to be the left of this
                    # position
                    posLeft = candidate.rfind(c, 0, matchPos[0])
                    if posLeft == -1:
                        return (False, [])
                    else:
                        return (False, [posLeft])
            else:
                sepScore = sepScore + 1 if candidate[pos -1] in sep else sepScore
                matchPos.append(pos)
                if len(matchPos) > 1:
                    clusterScore = clusterScore + matchPos[-1] - matchPos[-2] - 1
                left = pos + 1
                first = False
        return (True, matchPos, clusterScore, len(candidate) - matchPos[0], sepScore)

    didMatch = False
    l, r = 0, len(candidate)
    while not didMatch:
        didMatch, positions, *rest = walkString(query, candidate, l, r)
        if didMatch:
            break  # all done
        if not positions:
            break  # all done too - first char didn't match

        # resume search - start looking left from this position onwards
        r = positions[0]
    return (didMatch, positions, *rest)




def fuzzyMatches(query, candidates, limit, key=None):
    """Find fuzzy matches among given candidates

    :query: TODO
    :candidates: TODO
    :limit: TODO
    :returns: TODO

    """
    key = idfn if not key else key
    findFirstN = True
    count = 0
    for x in candidates:
        s = key(x)
        didMatch, positions, *rest = isMatch(query, s)
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

