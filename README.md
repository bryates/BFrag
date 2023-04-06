### Installing in CMSSW 10_6_X
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
git clone git@github.com:bryates/BFrag.git BFrag/BFrag
scram b -j8

cd BFrag/BFrag
```

### Submitting to CRAB
To submit a list of samples, described in a json file to the grid you can use the following script.
```
python scripts/submitToGrid.py -j data/UL/samples.json -c ${CMSSW_BASE}/src/BFrag/BFrag/test/runJetAnalyzer_cfg.py --lfn /store/group/phys_top/byates -s
```
### Running a local test
Initialize voms proxy (if needed):
```
voms-proxy-init --rfc --voms cms -valid 192:00
```
Run: 
```c++
cmsRun test/runJetAnalyzer_cfg.py maxEvents=10
root -l histo.root
root [1] ((TTree*)gDirectory->Get("data"))->Scan("j_pt:l_pt:l_id:l_pid:l_g_pt:l_g_id:l_relIso")
***********************************************************************************************************
*    Row   * Instance *      j_pt *      l_pt *      l_id *     l_pid *    l_g_pt *    l_g_id *  l_relIso *
***********************************************************************************************************
*        0 *        0 * 67.389404 * 56.023582 *       -11 *        15 * 54.975467 *       -11 * 0.0174571 *
*        0 *        1 * 56.712253 *           *           *           *           *           *           *
*        0 *        2 * 31.101026 *           *           *           *           *           *           *
*        0 *        3 * 28.338140 *           *           *           *           *           *           *
*        0 *        4 * 14.955394 *           *           *           *           *           *           *
*        0 *        5 * 11.322375 *           *           *           *           *           *           *
*        1 *        0 * 78.455833 * 51.896762 *        13 *        15 * 51.621730 *        13 *         7 *
*        1 *        1 * 73.810310 * 22.815336 *       -13 *        15 * 22.809196 *       -13 *         0 *
*        1 *        2 * 69.962585 * 43.241451 *        11 *         0 *           *           * 0.6815271 *
*        1 *        3 * 56.711021 *           *           *           *           *           *           *
*        1 *        4 * 30.348548 *           *           *           *           *           *           *
*        1 *        5 * 11.186533 *           *           *           *           *           *           *
*        2 *        0 * 255.34346 * 120.59804 *       -13 *        15 * 121.58523 *       -13 *         0 *
*        2 *        1 * 170.94065 * 14.367151 *        13 *        15 * 14.519094 *        13 *         0 *
*        2 *        2 * 54.502502 *           *           *           *           *           *           *
*        2 *        3 * 47.647289 *           *           *           *           *           *           *
*        2 *        4 * 25.089544 *           *           *           *           *           *           *
*        2 *        5 * 16.064987 *           *           *           *           *           *           *
*        2 *        6 * 15.146607 *           *           *           *           *           *           *
*        2 *        7 * 11.104058 *           *           *           *           *           *           *
***********************************************************************************************************
(long long) 20
```


### Install combine
```
cd $CMSSW_BASE/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
cd -
scram b -j8
```

### Running comibne
```
sh scripts/run_combine.sh
```
will make the datacard, the workspace, and run combine with the MultiDimFit option
