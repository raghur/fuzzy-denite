import sys
import itertools


def scorer(x):
    return len(x[0]) + 200 - x[2]  - x[3]


def scoreMatches(matches, limit):
    # return sorted(matches, key=lambda x: sum(x[1])/len(x[0]), reverse=True)
    return itertools.islice(sorted(matches, key=scorer, reverse=True), limit)


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
        pos = len(x)
        isMatch = True
        matchPos = []
        clusterScore = 0
        for c in reversed(query):
            try:
                pos = x.rindex(c, 0, pos)
                matchPos.append(pos)
                if len(matchPos) > 1:
                    clusterScore = clusterScore + (matchPos[-2] - pos - 1)
            except ValueError as v:
                isMatch = False
                break
        if isMatch:
            count = count + 1
            yield (x, matchPos, clusterScore, len(x) - matchPos[-1])
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

