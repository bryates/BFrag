import os
import glob
from itertools import chain
import json
import argparse
parser = argparse.ArgumentParser(description='You can select which file to run over')
parser.add_argument('--path',     nargs='+' , help = 'Path(s) to ROOT files', required=True)
parser.add_argument('--process',  nargs='+' , help = 'Process name(s)', required=True)
args = parser.parse_args()

for ipath,path in enumerate(args.path):
    fileset = {}
    paths = glob.glob(path)
    paths = [p for p in (chain.from_iterable(os.walk(path) for path in paths)) if 'log' not in p]
    d_path = paths[1][0]
    files = [d_path + fname for fname in paths[1][2]]
    fileset[args.process[ipath]] = files

    with open(f'{args.process[ipath]}.json', 'w') as fout:
        json.dump(fileset, fout, indent=4)
