#! /usr/bin/env python3
'''
Compute the correlation between two distance matrices using the Mantel test
http://scikit-bio.org/docs/0.1.3/generated/skbio.math.stats.distance.mantel.html
'''
from gzip import open as gopen
from skbio.stats.distance import mantel
from sys import argv

# parse tn93 file
def parse_tn93(fn):
    if fn.lower().endswith('.gz'):
        data = [l.strip() for l in gopen(fn).read().decode().strip().splitlines() if not l.startswith('ID1,')]
    else:
        data = [l.strip() for l in open(fn) if not l.startswith('ID1,')]
    dm = dict()
    for l in data:
        u,v,d = l.split(','); u = u.strip(); v = v.strip(); d = float(d)
        if u not in dm:
            dm[u] = dict()
        if v not in dm:
            dm[v] = dict()
        dm[u][v] = dm[v][u] = d
    IDs = list(dm.keys())
    return [[0 if u == v else dm[u][v] for v in IDs] for u in IDs]

# main functionality
if __name__ == "__main__":
    # check user args
    if len(argv) not in {3,4}:
        print("USAGE: %s <tn93_dists_1> <tn93_dists_2> [spearman,pearson]" % argv[0]); exit(1)
    if len(argv) == 3:
        method = 'spearman'
    else:
        if argv[3].lower() not in {'pearson','spearman'}:
            print("Invalid mode: %s (options: spearman, pearson)" % argv[3]); exit(1)
        method = argv[3].lower()

    # parse distance matrices
    dm1 = parse_tn93(argv[1])
    dm2 = parse_tn93(argv[2])
    coeff, p_value, n = mantel(dm1, dm2, method=method, permutations=0)
    print("%s Correlation: %f" % (method.capitalize(), coeff))
    #print("p-Value: %f" % p_value)
