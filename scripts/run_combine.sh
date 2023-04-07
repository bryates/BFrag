#!/bin/bash
echo "Making the datacard"
python3 scripts/make_card.py 

echo "Processing the model"
text2workspace.py rb_card.txt -P BFrag.BFrag.rbModel:rbmodel --PO fits=rb_param.npy --X-allow-no-background --X-allow-no-signal

echo "Running combine"
IFS='\n'
combine_out=`combine -d rb_card.root -M MultiDimFit --setParameters rb=0.855 --saveFitResult 2>&1`
echo $combine_out | grep -e "rb :"
combine_out=`combine -d rb_card.root -M FitDiagnostics --setParameters rb=0.855 2>&1`
echo $combine_out | grep -e "Best fit rb"
