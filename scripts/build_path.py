import os
import glob
from itertools import chain
import json
import argparse
parser = argparse.ArgumentParser(description='You can select which file to run over')
parser.add_argument('--path', help = 'Path(s) to ROOT files', required=True)
parser.add_argument('--json', default='card_mc16.yml', help = 'JSON file of samples', required=True)
parser.add_argument('--out',  default='mc_UL16.json', help = 'JSON file of samples',)
args = parser.parse_args()

fin = open(args.json)
infiles = json.load(fin)

fileset = {}
for ifilename,filename in enumerate(infiles):
    fileset[infiles[filename] + '_16'] = []
    fileset[infiles[filename] + '_16APV'] = []
    fileset[infiles[filename] + '_17'] = []
    fileset[infiles[filename] + '_18'] = []
    for path in glob.iglob(f'{args.path}/{filename}/**/*.root', recursive=True):
        path = path.replace('//', '/')
        #paths = [p for p in (chain.from_iterable(os.walk(path) for path in paths)) if 'log' not in p]
        #d_path = paths[1][0]
        #files = [f'{d_path}/{fname}' for fname in paths[1][2]]
        #files = [f'{d_path}/{fname}' for fname in paths[1][2]]
        year = path.split('UL')[1][:2]
        if 'APV' in path:
            year = year + 'APV'
        fileset[infiles[filename]+'_'+year].append(path)

with open(f'{args.out}', 'w') as fout:
    json.dump(fileset, fout, indent=4)
