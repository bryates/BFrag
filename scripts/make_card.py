import uproot
import numpy as np
import os

param = { 655: 'sdown', 700: '700', 725: '725', 755: 'down', 775: 'dddown', 825: 'scentral', 855: '', 875: 'cccentral', 900: 'ccentral', 955: 'central', 975: 'uuup', 1000: 'uup'}
#param = { 655: 'sdown', 700: '700', 725: '725', 755: 'down', 775: 'dddown', 800: 'ddown', 825: 'scentral', 855: '', 875: 'cccentral', 9: 'ccentral', 925: '925', 955: 'central', 975: 'uuup', 1.000: 'uup', 1.055: 'up'}

channels = ['d0', 'd0_mu_tag_mu', 'jpsi']
channels = ['d0']
chan_fits = []
chan_data = []
masks = []
mask_edge = 0.56

for channel in channels:
    fname = f'/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_172v5_Bfrag_genreco_sPlot_{channel}1_xb.root'
    frac = 'ptfrac_signal_hist'
    if 'mu_tag' in fname:
        fname = fname.replace('_xb', '_inc')
    with uproot.open(fname) as fin:
        frag_hist_BF = fin[frac].to_numpy()[0][1:]
        edges = fin[frac].to_numpy()[1][1:]
    fname = f'/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_172v5_Bfrag_genreco_sPlot_{channel}2_xb.root'
    if 'mu_tag' in fname:
        fname = fname.replace('_xb', '_inc')
    with uproot.open(fname) as fin:
        frag_hist_GH = fin[frac].to_numpy()[0][1:]
    
    fname = f'/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_Data_Bfrag_genreco_sPlot_{channel}1_xb.root'
    if 'mu_tag' in fname:
        fname = fname.replace('_xb', '_inc')
    with uproot.open(fname) as fin:
        data_hist_BF = fin[frac].to_numpy()[0][1:]
    fname = f'/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_Data_Bfrag_genreco_sPlot_{channel}2_xb.root'
    if 'mu_tag' in fname:
        fname = fname.replace('_xb', '_inc')
    with uproot.open(fname) as fin:
        data_hist_GH = fin[frac].to_numpy()[0][1:]

    mask = edges[:-1] > mask_edge
    masks.append(mask)
    edges = edges[edges>mask_edge]
    
    mc_norm = np.sum(frag_hist_BF + frag_hist_GH)
    data_norm = np.sum(data_hist_BF + data_hist_GH)
    
    frag_hist_BF = frag_hist_BF[mask]
    frag_hist_GH = frag_hist_GH[mask]
    data_hist_BF = data_hist_BF[mask]
    data_hist_GH = data_hist_GH[mask]
    chan_fits.append(frag_hist_BF + frag_hist_GH)
    chan_data.append(data_hist_BF + data_hist_GH)

nprocs = 1
nsysts = 0
space = '----------------------------------------------------------------------------------------------------------------------------------\n'
with open('rb_card.txt', 'w') as card:
    card.write('Datacard for rb fitting\n')
    bins = np.array([ch.shape[0]-1 for ch in chan_fits])
    nbins = np.sum(bins)
    card.write('imax {} number of bins\n'.format(nbins))
    card.write('jmax {} number of processes minus 1\n'.format(len(channels)-1))
    card.write('kmax {} number of nuisance paramters\n'.format(nsysts))
    card.write(space)
    for ibin in range(nbins):
        card.write(f'shapes * bin{ibin+1} FAKE\n')
    card.write(space)
    card.write('bin\t\t\t\t\t')
    for ibin in range(nbins):
        card.write('bin{}\t\t\t\t\t'.format(ibin+1))
    card.write('\n')
    card.write('observation\t\t\t')
    for iproc in range(len(channels)):
        for ibin in range(bins[iproc]):
            card.write('{}\t\t\t\t\t\t'.format(chan_data[iproc][ibin]))
    card.write('\n')
    card.write(space)
    card.write('bin\t\t\t\t\t')
    for iproc,fit in enumerate(chan_fits):
        offset = iproc * bins[iproc]
        for ibin in range(bins[iproc]):
            card.write('bin{}\t\t\t\t\t'.format(ibin+offset+1))
    card.write('\n')
    card.write('process\t\t\t\t')
    for iproc,fit in enumerate(chan_fits):
        for ibin in range(bins[iproc]):
            card.write('{}\t\t\t\t\t'.format(channels[iproc]))
    card.write('\n')
    card.write('process\t\t\t\t')
    for iproc,fit in enumerate(chan_fits):
        for ibin in range(bins[iproc]):
            card.write('{}\t\t\t\t\t'.format(-1*(iproc+1)))
    card.write('\n')
    card.write('rate\t\t\t\t')
    for iproc,fit in enumerate(chan_fits):
        for ibin in range(bins[iproc]):
            card.write('{}\t\t\t\t\t\t'.format(1))
            #card.write('{}\t\t\t\t\t\t'.format(frag_hist_BF[ibin] + frag_hist_GH[ibin]))

bin_vals = list()
size = 0
#widths = np.array([edges[i] - edges[i-1] for i in range(1, edges.shape[0])])
rb_out = {}
for ichan,channel in enumerate(channels):
    rb_vals = []
    for rb in param:
        fname = '/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_172v5_Bfrag_genreco_{}_sPlot_d01_xb.root'.format(param[rb])
        if not os.path.exists(fname):
            continue
        if rb == 855:
            fname = '/afs/cern.ch/user/b/byates/TopAnalysis/LJets2015/2016/mtop/sPlot/sPlot/TopMass_172v5_Bfrag_genreco_sPlot_d01_xb.root'
        rb_vals.append(rb/1000.)
        with uproot.open(fname) as fin:
            tmp_vals = fin['ptfrac_signal_hist'].values()
        size = len(tmp_vals)
        fname = fname.replace('1_xb', '2_xb')
        with uproot.open(fname) as fin:
            tmp_vals += fin['ptfrac_signal_hist'].values()
        tmp_vals /= np.sum(tmp_vals) # Normalize to parameterize shape only
        tmp_vals *= data_norm
        tmp_vals = tmp_vals[masks[ichan]]
        #tmp_vals /= widths[:-1] # Divide by bin widths
        if rb == list(param.keys())[0]:
            bin_vals = tmp_vals
        else:
            bin_vals = np.vstack((bin_vals,tmp_vals))
    
    for ibin in range(bin_vals.shape[1]):
        rb_out['bin{}_{}'.format(ibin+1,channel)] = np.polyfit(rb_vals, bin_vals[:,ibin], 1)

np.save('rb_param', rb_out)
