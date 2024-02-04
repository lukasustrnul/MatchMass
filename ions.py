# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:13:31 2024

@author: Lukáš Ustrnul
"""
import numpy as np
# Data needed for calculations of molecular masses and so on.

# dictionary for particle provided by user
M_orig = {'ion':'[M]','add_mass':0, 'multiply_by':1, 'charge':np.nan, 'add_to_df':False}

# list of ions as a dictionaries:
Mplus = {'ion':'[M]+','add_mass':-0.00054858026, 'multiply_by':1, 'charge':'1+', 'add_to_df':True}
MplusH = {'ion':'[M+H]+','add_mass':+1.007276, 'multiply_by':1, 'charge':'1+', 'add_to_df':True} 
MplusNa = {'ion':'[M+Na]+','add_mass':+22.989218, 'multiply_by':1, 'charge':'1+', 'add_to_df':True}
MplusK = {'ion':'[M+K]+','add_mass':+38.963158, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
MplusNH4 = {'ion':'[M+NH4]+','add_mass':+18.033823, 'multiply_by':1, 'charge':'1+', 'add_to_df':False}
Mplus2H = {'ion':'[M+2H]2+','add_mass':+1.007276, 'multiply_by':0.5, 'charge':'2+', 'add_to_df':False}
M2plusH = {'ion':'[2M+H]+','add_mass':+1.007276, 'multiply_by':2, 'charge':'1+', 'add_to_df':True}
Mplus3H = {'ion':'[M+3H]3+','add_mass':+1.007276, 'multiply_by':0.3333333, 'charge':'3+', 'add_to_df':False}
MminusH = {'ion':'[M-H]-','add_mass':-1.007276, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}
M2minusH = {'ion':'[2M-H]-','add_mass':-1.007276, 'multiply_by':2, 'charge':'1-', 'add_to_df':False}
Mminus2H = {'ion':'[M-2H]2-','add_mass':-1.007276, 'multiply_by':0.5, 'charge':'2-', 'add_to_df':False}
MplusCl = {'ion':'[M+Cl]-','add_mass':+34.969402, 'multiply_by':1, 'charge':'1-', 'add_to_df':False}

# make a list of all dictionaries
ion_list = [M_orig, Mplus, MplusH, MplusNa, MplusK, MplusNH4, Mplus2H, M2plusH, Mplus3H, MminusH, M2minusH, Mminus2H, MplusCl]
pos_ion_list = [Mplus, MplusH, MplusNa, MplusK, MplusNH4, Mplus2H, M2plusH, Mplus3H]
neg_ion_list = [MminusH, M2minusH, Mminus2H, MplusCl]


