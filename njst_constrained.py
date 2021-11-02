import asterid as ad
import nj
import treeswift as ts
import argparse

def starlize(tree):
    tocontract = []
    for n in tree.traverse_preorder(leaves=False,internal=True):
        tocontract.append(n)
    for n in tocontract:
        n.contract()
    return tree

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run ASTRID')
    parser.add_argument("-i", "--input", type=str,
                        help="Input tree list file", required=True)
    parser.add_argument("-o", "--output", type=str,
                        help="Output tree file", required=True)
    parser.add_argument("-j", "--tree", type=str, help="constraint trees")
    args = parser.parse_args()
    tree = None
    if args.tree:
        with open(args.tree) as fh:
            tree = ts.read_tree_newick(fh.read())
    else:
        with open(args.input, "r") as fh:
            for l in fh:
                tree = ts.read_tree_newick(l)
                starlize(tree)
                break
    with open(args.input, "r") as o: genes = o.readlines()
    ts = ad.get_ts(genes)
    D = ad.mk_distance_matrix(ts, genes)
    merged_tree = nj.treeresolve_lua(tree, ts, D)
    res = merged_tree.newick()
    if args.output == "-":
        print(res)
    else:
        with open(args.output, "w+") as outf:
            outf.write(res)