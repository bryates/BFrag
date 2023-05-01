import coffea
import coffea.util
import hist
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
from scipy.stats import chi2
import uproot

output = {}
sumw = 0
sumw2 = 0

# Load all pkl files into memory
count = 0
total = 670
for ifile in range(total):
    name = f'histos/coffea_{ifile}.pkl'
    if not os.path.exists(name):
        print(f'Skipping {name}!')
        continue
    fin = coffea.util.load(name)
    for key in fin.keys():
        if key in output:
            output[key] += fin[key]
        else:
            output[key] = fin[key]
    sumw += fin['sumw']['ttbar']
    sumw2 += fin['sumw2']['ttbar']
    count += 1
print(f'Loaded {count} / {total}')

# Scale processes by cross-section
xsecs = {'ttbar': 830}
for key in output:
    if 'sumw' in key:
        continue #sumw and sumw2 are dicts, not hists
    for iax,ax in enumerate(list(output[key].axes[0])):
        output[key].view(flow=True)[iax] *= 135 * 1000 * xsecs[ax] / sumw

# Save the total histograms in a pkl file and a ROOT file for testing
coffea.util.save(output, 'coffea.pkl')
with uproot.recreate('output.root') as fout:
    for key in output:
        if 'sumw' in key:
            continue #sumw and sumw2 are dicts, not hists
        for s in output[key].axes['dataset']:
            fout[ f'histo/{key}_{s}'] = output[key][{'dataset': s}]
            #h = output[key][{'dataset': s}]
            #fout[f'histo/{key}_{s}'] = h * 135 * 1000 * xsecs[s] / sumw


def d0_mass_fit(mass, mean, sigma, nsig, mean_kk, sigma_kk, nkk, mean_pp, sigma_pp, npp, l, nbkg):
    '''
    Define function for fitting D0 mass peak
    Peak Gaussian + exponential bkg + D0 -> KK Gaussian + D0 -> pipi Gaussian
    '''
    return \
    nsig * np.exp(-1/2 * (np.square(mass - mean) / np.square(sigma))) + \
    nkk  * np.exp(-1/2 * (np.square(mass - mean_kk) / np.square(sigma_kk))) + \
    npp  * np.exp(-1/2 * (np.square(mass - mean_pp) / np.square(sigma_pp))) + \
    nbkg * np.exp(l * mass)

mass_bins = np.linspace(1.7, 2.0, 31)
xb_bins = np.linspace(0, 1, 11)

meson_tex = {'d0': '$\mathrm{D^{0}}$', 'jpsi': '$\mathrm{J/\psi}$'}

def plot_mass(meson='d0'):
    '''
    Plot and fit the specified meson mass
    '''
    print(f'Fitting {meson}')
    xb_mass = []
    output[f'xb_mass_{meson}'] *=  135 * 1000 * 832. / sumw
    h = output[f'xb_mass_{meson}'][{'dataset': sum}]
    h.plot2d()
    plt.savefig(f'xb_mass_{meson}.png')
    plt.close()
    output[f'xb_mass_{meson}'] *=  135 * 1000 * 832. / sumw
    h = output[f'xb_mass_{meson}']
    xb_bins = h.axes[1].edges
    for ibin in range(0,xb_bins.shape[0]-1):
        #output[f'd0_{ibin}'] *= 135 * 1000 * 832./sumw
        #h_d0 = output[f'{meson}_{ibin}'].values()[0]
        x = h[{'xb': slice(hist.loc(xb_bins[ibin]), hist.loc(xb_bins[ibin+1]), sum)}]
        '''
        if np.sum(x.values()[0]) < 1:
            continue
        '''
        x.plot1d(label=f'{meson_tex[meson]} {ibin}')
        #plt.step(mass_bins[:-1], h_d0, label=f'D0 {ibin}')
    plt.legend()
    plt.savefig(f'{meson}_mass.png')
    plt.close()
    output[f'{meson}_mass'].plot1d(label=f'{meson_tex[meson]} mass')
    output[f'xb_mass_{meson}'][{'xb': sum}].plot1d(label=f'{meson_tex[meson]} mass 1D')
    plt.legend()
    plt.savefig(f'{meson}_mass_full.png')
    plt.close()
    
    
    mes = meson.replace('_','')
    output[f'xb_{mes}'].plot1d(label='$x_{\mathrm{b}}$')
    #plt.step(x=xb_bins[:-1], y=output[f'xb_{mes}'], label='$x_{\mathrm{b}}$')
    plt.legend()
    plt.savefig(f'xb_{meson}_all.png')
    plt.close()
    
    if meson != 'd0':
        return

    output[f'vtx_mass_{meson}'] *=  135 * 1000 * 832. / sumw
    h = output[f'vtx_mass_{meson}'][{'dataset': sum}]
    h.plot2d()
    plt.savefig(f'vtx_mass_{meson}.png')
    plt.close()

d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0 = 1.87, .01, 0, 1.78, 0.02, 0, 1.9, 0.02, 0, -2.27, 30
def plot_and_fit_mass(meson='d0'):
    '''
    Plot and fit the specified meson mass
    '''
    print(f'Fitting {meson}')
    xb_mass = []
    bins = []
    output[f'xb_{meson}'] *=  135 * 1000 * 832. / sumw
    output[f'xb_mass_{meson}'] *=  135 * 1000 * 832. / sumw
    #FIXME output[f'xb_{meson}'] *=  135 * 1000 * 832. / sumw
    h = output[f'xb_mass_{meson}']
    #for ibin in range(1,10):
        #output[f'd0_{ibin}'] *= 135 * 1000 * 832./sumw
        #h_d0 = output[f'{meson}_{ibin}'].values()[0]
    for ibin in range(0,xb_bins.shape[0]-1):
        #output[f'd0_{ibin}'] *= 135 * 1000 * 832./sumw
        #h_d0 = output[f'{meson}_{ibin}'].values()[0]
        x = h[{'xb': slice(hist.loc(xb_bins[ibin]), hist.loc(xb_bins[ibin+1]), sum)}].values()[0]
        #FIXME x = output[f'xb_{meson}'].values()[0]
        ne0 = np.sum(x)*2
        if ne0 < 21:
            xb_mass.append(0)
            bins.append(xb_bins[ibin])
            print(f'Warning, not enough events found in {meson} bin {ibin}!')
            continue
        nd0 = .001 * ne0
        npp = .1 * nd0
        nkk = .1 * nd0
        plt.step(mass_bins[:-1], x, label=f'{meson_tex[meson]} {np.round(xb_bins[ibin], 1)} < ' + '$x_{\mathrm{b}}$' + f' < {np.round(xb_bins[ibin+1], 1)}')
        g = [d0_mass_fit(x, d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0) for x in mass_bins]
        try:
            popt, pcov = curve_fit(d0_mass_fit, mass_bins[:-1], x, p0=[d0_mean0, d0_sigma0, nd0, kk_mean0, kk_sigma0, nkk, pp_mean0, pp_sigma0, npp, l0, ne0], bounds=([1.85, 0, 0, 1.77, 0, 0, 1.88, 0, 0, -10, 0], [1.88, .02, ne0, 1.79, .02, ne0, 1.91, .02, ne0, 10, ne0]))
        except:
            continue
        plt.plot(mass_bins, d0_mass_fit(mass_bins, *popt), label=f'Fit {ibin}')
        print(f'N D0 {round(popt[2])} +/- {round(np.sqrt(pcov[2][2]))}, N bkg {round(popt[10])} +/- {round(np.sqrt(pcov[10][10]))}')
        xb_mass.append(popt[2])
        bins.append(xb_bins[ibin])
        chisq = np.sum(np.nan_to_num(np.square(x - d0_mass_fit(mass_bins, *popt)[:-1]) / x, 0, posinf=0, neginf=0))
        #print(f'Chi^2 = {chisq} P = {chi2.cdf(chisq, 30)}')
    plt.legend(ncol=3, bbox_to_anchor=(-0.1, 1.15), loc='upper left', borderaxespad=0.)
    plt.savefig(f'{meson}_mass_fit.png')
    plt.close()
    plt.step(x=bins, y=xb_mass, label='$x_{\mathrm{b}}$ signal')
    #plt.step(x=xb_bins[:-1], y=xb_mass, label='$x_{\mathrm{b}}$ signal')
    #plt.hist(xb_mass, label='$x_{\mathrm{b}}$ signal')
    plt.legend()
    plt.savefig(f'xb_{meson}_sig.png')
    plt.close()


plot_and_fit_mass('d0')
plot_mass('d0') # Not enough statistics to fit D0mu mass peak?
plot_mass('jpsi') # Not enough statistics to fit D0mu mass peak?
plot_mass('d0_mu') # Not enough statistics to fit D0mu mass peak?