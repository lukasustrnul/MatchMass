"""
Author: Lukáš Ustrnul
GitHub: https://github.com/lukasustrnul
LinkedIn: https://www.linkedin.com/in/luk%C3%A1%C5%A1-ustrnul-058420123/

File: ions_enum.py
Created on 16.03.2024
"""
from typing import NamedTuple
from enum import Enum
import numpy as np


class IonInfo(NamedTuple):
    """
    Namedtuple to improve calls for ion information.
    """
    ion_formula: str
    add_mass: float
    multiply_by: float
    charge: str
    ion_type: str
    neutral_loss: bool
    neutral_loss_molecule: str


class Ion(Enum):
    """
    A custom class inheriting from Enum. Stores ion information which can be used to calculate molecular masses.
    """

    # dictionary for particle provided by user
    M_orig = IonInfo('use uploaded theoretical m/z',  0,  1.0, np.nan, 'provided_by_user', False, '')
    
    # cations
    Mplus = IonInfo('M+', -0.00054858026, 1.0, '1+', 'cation', False, '')
    MplusH = IonInfo('[M+H]+', +1.007276, 1.0, '1+', 'cation', False, '')
    MplusNa = IonInfo('[M+Na]+', +22.989218, 1.0, '1+', 'cation', False, '')
    MplusK = IonInfo('[M+K]+', +38.963158, 1.0, '1+', 'cation', False, '')
    MplusNH4 = IonInfo('[M+NH4]+', +18.033823, 1.0, '1+', 'cation', False, '')
    Mplus2H = IonInfo('[M+2H]2+', +1.007276, 0.5, '2+', 'cation', False, '')
    M2plusH = IonInfo('[2M+H]+', +1.007276, 2.0, '1+', 'cation', False, '')
    MplusHplusNa = IonInfo('[M+H+Na]2+', +11.998247, 0.5, '2+', 'cation', False, '')
    Mplus2Na = IonInfo('[M+2Na]2+', +22.989218, 0.5, '2+', 'cation', False, '')
    Mplus3H = IonInfo('[M+3H]3+', +1.007276, 0.3333333, '3+', 'cation', False, '')

    # neutral losses cations
    MminusH20plusH = IonInfo('[M-H2O+H]+ (neutral loss)', -17.003284, 1.0, '1+', 'cation', True, 'H2O')
    MminusH20plusNa = IonInfo('[M-H2O+Na]+ (neutral loss)', +4.978658, 1.0, '1+', 'cation', True, 'H2O')
    
    # anions
    MminusH = IonInfo('[M-H]-', -1.007276, 1.0, '1-', 'anion', False, '')
    M2minusH = IonInfo('[2M-H]-', -1.007276, 2.0, '1-', 'anion', False, '')
    Mminus2H = IonInfo('[M-2H]2-', -1.007276, 0.5, '2-', 'anion', False, '')
    MplusCl = IonInfo('[M+Cl]-', +34.969402, 1.0, '1-', 'anion', False, '')
    MplusBr = IonInfo('[M+Br]-', +78.918885, 1.0, '1-', 'anion', False, '')
    MplusFA = IonInfo('[M+HCOO]-', +44.998201, 1.0, '1-', 'anion', False, '')
    MplusAc = IonInfo('[M+CH3COO]-', +59.013851, 1.0, '1-', 'anion', False, '')
    MplusTFA = IonInfo('[M+CF3COO]-', +112.985589, 1.0, '1-', 'anion', False, '')


if __name__ == '__main__':
    pass
