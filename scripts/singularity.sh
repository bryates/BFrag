#!/usr/bin/env bash

echo "Untarring the virtual environment"
# Do this *not* verbose
#cp -Rp /afs/cern.ch/user/b/byates/CMSSW_10_6_18/src/BFrag/BFrag/myenv.tgz .
#tar -zxf myenv.tgz
echo

echo `pwd`
echo "Activating our virtual environment"
#source myenv/bin/activate
echo

echo "Running our python example!"
#python coffea_test.py
python CharmJet.py --ifile $2
echo

echo "All done!"
