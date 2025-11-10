import numpy as np 

def compute_electric_field(phi, dx=1.0, dy=1.0):
    Ex = -(phi[2:, 1:-1] - phi[:-2, 1:-1]) / (2 * dx)
    Ey = -(phi[1:-1, 2:] - phi[1:-1, :-2]) / (2 * dy)

    return Ex, Ey
