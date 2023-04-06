import numpy as np
from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel

class rbModel(PhysicsModel):
    '''
    text2workspace.py card.txt -P BFrag.BFrag.rbModel:rbmodel --PO fits=rb_param.npy --X-allow-no-background

    >>> import numpy as np
    >>> fit = {'bin1': (10 - (.855*.1), 0.1), 'bin2': (15 - (.855*.01), 0.01), 'bin3': (50 - (.855*0.12), 0.012)}
    >>> np.save('rb_param', fit)

    '''

    def setPhysicsOptions(self, options):
        self.procbins = []

        for option, value in [x.split('=') for x in options]:
            if option == 'fits': # .npy fit file created with FitConversion16D.py
                self.fits = value

        fits = np.load(self.fits)[()]
        self.procbins.extend(fits.keys())

    def setup(self):
        fits = np.load(self.fits)[()]
        for i,proc in enumerate(self.procbins):
            name = 'r_{proc}'.format(proc=proc)
            fit_terms = '{}*rb+{}'.format(fits[proc][0], fits[proc][1])
            fit_function = "expr::{name}('{fit_terms}',rb)".format(name=name, fit_terms=fit_terms)
            func = self.modelBuilder.factory_(fit_function)
            self.modelBuilder.out._import(func)
    
    def doParametersOfInterest(self):
        self.modelBuilder.doVar('rb[0.855, 0.6, 1.0]')
        self.modelBuilder.doSet('POI', 'rb')
        self.setup()
    
    def getYieldScale(self, bin, process):
        if 'ttbar' not in process:
            return 1
        else:
            name = 'r_{}_{}'.format(bin,process)
            return name

rbmodel = rbModel()
