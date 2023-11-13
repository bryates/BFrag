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
    isData = False
    fname = infiles[filename]
    if any(data in infiles[filename] for data in ['EG','Muon', 'Electron']):
        isData = True
        fileset['Data13TeV_'+infiles[filename]+'_'+filename.split('UL')[1].split('_')[0][2:]] = []
    else:
        fileset[infiles[filename] + '_16'] = []
        fileset[infiles[filename] + '_16APV'] = []
        fileset[infiles[filename] + '_17'] = []
        fileset[infiles[filename] + '_18'] = []
    for path in glob.iglob(f'{args.path}/{fname}/**/*.root', recursive=True):
        path = path.replace('//', '/')
        year = path.split('UL')[1][:2] if not isData else path.split('UL')[1].split('_')[0][2:]
        if 'APV' in path:
            year = year + 'APV'
        if not isData:
            fileset[infiles[filename]+'_'+year].append(path)
        else:
            fileset['Data13TeV_'+infiles[filename]+'_'+year].append(path)

with open(f'{args.out}', 'w') as fout:
    json.dump(fileset, fout, indent=4)
