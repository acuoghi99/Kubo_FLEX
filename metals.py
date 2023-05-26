import numpy as np

# CONSTANTS (SI)
e     = 1.602176634e-19 # C   - fundamental charge
m_e   = 9.1093837e-31 # kg    - electron mass
kB    = 1.380649e-23 # J/K    - Boltzmann's constant
hbar  = 1.054571817e-34 # J*s - reduced Planck's constant
mu0   = 1.256637e-6 # N*A⁻²   - vacuum magnetic permeability

metals = {'Tl2201': {'a': 3.87, 'b': 3.87, 'c': 11.60,
               'p=0.12' : {'mu': 0.1998, 't1':-0.7250, 't2': 0.3020, 't3': 0.0159, 't4': 0.0805, 't5': 0.0034},
               'p=0.25' : {'mu': 0.2382, 't1':-0.7250, 't2': 0.3020, 't3': 0.0159, 't4': 0.0805, 't5': 0.0034}},

          'LSCO' : {'a': 3.76, 'b': 3.76, 'c': 6.61,
               'p=0.12' : {'mu': 0.1952, 't1':-1.0000, 't2': 0.1656, 't3':-0.0828, 't4': 0.0800, 't5': 0.0000},
               'p=0.16' : {'mu': 0.2025, 't1':-1.0000, 't2': 0.1500, 't3':-0.0750, 't4': 0.0800, 't5': 0.0000},
               'p=0.20' : {'mu': 0.2118, 't1':-1.0000, 't2': 0.1376, 't3':-0.0688, 't4': 0.0800, 't5': 0.0000},
               'p=0.23' : {'mu': 0.2201, 't1':-1.0000, 't2': 0.1304, 't3':-0.0652, 't4': 0.0800, 't5': 0.0000},
               'p=0.24' : {'mu': 0.2231, 't1':-1.0000, 't2': 0.1284, 't3':-0.0642, 't4': 0.0800, 't5': 0.0000},
               'p=0.28' : {'mu': 0.2365, 't1':-1.0000, 't2': 0.1224, 't3':-0.0612, 't4': 0.0800, 't5': 0.0000},
               'p=0.32' : {'mu': 0.2519, 't1':-1.0000, 't2': 0.1195, 't3':-0.0597, 't4': 0.0800, 't5': 0.0000}},

          'Nd-LSCO' : {'a': 3.75, 'b': 3.75, 'c': 6.60,
               'p=0.24' : {'mu': 0.1319, 't1':-0.6400, 't2': 0.0873, 't3':-0.0437, 't4': 0.0000, 't5': 0.0000}},

          'Bi2201' : {'a': 3.79, 'b': 3.79, 'c': 12.31,
               'p=0.08' : {'mu': 0.1338, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000},
               'p=0.12' : {'mu': 0.1600, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000},
               'p=0.16' : {'mu': 0.1846, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000},
               'p=0.20' : {'mu': 0.2074, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000},
               'p=0.24' : {'mu': 0.2283, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000},
               'p=0.28' : {'mu': 0.2472, 't1':-0.8800, 't2': 0.1373, 't3':-0.1439, 't4': 0.0573, 't5': 0.0000}}}

class Metal():
    """
    Class used to plot useful quantities of the system, as the energy dispersion,
    the Fermi surface, the velocities and the density of states.
    """
    
    def __init__(self, met, p):
        try: 
            self.met = metals[met]
        except KeyError as error_msg: 
            err_str = f"The metal {error_msg} is not implemented yet: possible values are {list(metals.keys())}"
            raise KeyError(err_str)
            
        self.p = str(p)
        self.a, self.b, self.c = self.get_lattice_vectors()
        self.s_coeff = self.get_s_coeff()
        
    def get_lattice_vectors(self):
        return self.met['a']/1e10, self.met['b']/1e10, self.met['c']/1e10 
    
    def get_TB_params(self):
        try: 
            met = self.met['p='+self.p]
        except KeyError as error_msg:
            err_str = f"The doping value {error_msg} is not implemented yet: possible values are {list(self.met.keys())[3:]}"
            raise KeyError(err_str)
            
        return met['mu']*e, met['t1']*e, met['t2']*e, met['t3']*e, met['t4']*e, met['t5']*e
    
    def get_s_coeff(self):
        a, b, c = self.get_lattice_vectors()
        mu, t1, t2, t3, t4, t5 = self.get_TB_params()
        return np.array([a, b, c, mu, t1, t2, t3, t4, t5])