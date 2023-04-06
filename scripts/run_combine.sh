#!/bin/bash
echo "Making the datacard"
python3 scripts/make_card.py 

echo "Processing the model"
text2workspace.py rb_card.txt -P BFrag.BFrag.rbModel:rbmodel --PO fits=rb_param.npy --X-allow-no-background --X-allow-no-signal

echo "Running combine"
combine -d rb_card.root -M MultiDimFit --setParameters rb=0.855
