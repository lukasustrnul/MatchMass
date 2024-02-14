# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:13:31 2024

@author: Lukáš Ustrnul
"""
import numpy as np
# Data needed for calculations of molecular masses and so on.

# dictionary for particle provided by user
M_orig = {'ion':'use uploaded theoretical m/z','add_mass':0, 'multiply_by':1, 'charge':np.nan, 'add_to_df':False}

# list of ions as a dictionaries:
# cations
Mplus = {'ion':'M+','add_mass':-0.00054858026, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
MplusH = {'ion':'[M+H]+','add_mass':+1.007276, 'multiply_by':1, 'charge':'1+', 'add_to_df':False} 
MplusNa = {'ion':'[M+Na]+','add_mass':+22.989218, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
MplusK = {'ion':'[M+K]+','add_mass':+38.963158, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
MplusNH4 = {'ion':'[M+NH4]+','add_mass':+18.033823, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
Mplus2H = {'ion':'[M+2H]2+','add_mass':+1.007276, 'multiply_by':0.5, 'charge':'2+', 'add_to_df':False}
M2plusH = {'ion':'[2M+H]+','add_mass':+1.007276, 'multiply_by':2, 'charge':'1+', 'add_to_df':False}
MplusHplusNa = {'ion':'[M+H+Na]2+','add_mass':+11.998247 , 'multiply_by':0.5, 'charge':'2+', 'add_to_df':False}
Mplus2Na = {'ion':'[M+2Na]2+','add_mass':+22.989218, 'multiply_by':0.5, 'charge':'2+', 'add_to_df':False}
Mplus3H = {'ion':'[M+3H]3+','add_mass':+1.007276, 'multiply_by':0.3333333, 'charge':'3+', 'add_to_df':False}
# neutral losses cations
MminusH20plusH = {'ion':'[M-H2O+H]+ (neutral loss)','add_mass':-17.003284, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
MminusH20plusNa = {'ion':'[M-H2O+Na]+ (neutral loss)','add_mass':+4.978658, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
# anions
MminusH = {'ion':'[M-H]-','add_mass':-1.007276, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}
M2minusH = {'ion':'[2M-H]-','add_mass':-1.007276, 'multiply_by':2, 'charge':'1-', 'add_to_df':False}
Mminus2H = {'ion':'[M-2H]2-','add_mass':-1.007276, 'multiply_by':0.5, 'charge':'2-', 'add_to_df':False}
MplusCl = {'ion':'[M+Cl]-','add_mass':+34.969402, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}
MplusFA = {'ion':'[M+FA]-','add_mass':+44.998201, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}
MplusAc = {'ion':'[M+Ac]-','add_mass':+59.013851, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}




# make a list of all dictionaries
ion_list = [M_orig, Mplus, MplusH, MplusNa, MplusK, MplusNH4, Mplus2H, M2plusH, MplusHplusNa, Mplus2Na, Mplus3H, MminusH20plusH, MminusH20plusNa, MminusH, M2minusH, Mminus2H, MplusCl, MplusFA, MplusAc]
pos_ion_list = [Mplus, MplusH, MplusNa, MplusK, MplusNH4, M2plusH, Mplus2H, MplusHplusNa, Mplus2Na, Mplus3H, MminusH20plusH, MminusH20plusNa]
neg_ion_list = [MminusH, M2minusH, Mminus2H, MplusCl, MplusFA, MplusAc]


