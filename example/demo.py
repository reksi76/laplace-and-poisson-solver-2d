import os
import sys
import numpy as np 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.boundary import set_plate_bc
from src.fields import compute_electric_field
from src.solver import laplace_jacobi, laplace_gauss_seidel,poisson_jacobi, poisson_gauss_seidel
from src.visualize import plot_heatmap, plot_quiver, animate_solution

nx = 50
ny = 50
V0 = 100.0

phi = np.zeros((nx, ny))

print("""
Modes:
 - top_hot
 - sinusoidal_hot
 - center_hot
 - circle_hot
""")
mode = str(input('Enter mode: '))
print("""Solver:
            1. jacobi 
            2. gauss seidel 
      """)
solver = input('Enter solver (1/2): ').strip()

mode = mode.strip().replace(' ', '_').lower()

phi, fixed_mask, source_term = set_plate_bc(nx, ny, mode)
poisson_mode = ['center_hot', 'circle_hot']

if mode in poisson_mode:
    if solver == '1':
        it, phi, history = poisson_jacobi(phi, source_term, fixed_mask=fixed_mask)
    elif solver == '2':
        it, phi, history = poisson_gauss_seidel(phi, source_term, fixed_mask=fixed_mask)
    else:
        raise ValueError('Error! Invalid solver choice')

else:
    if solver == '1':
        phi[-1,:] = 100.0
        it, phi, history = laplace_jacobi(phi, fixed_mask=fixed_mask)
    elif solver == '2':
        it, phi, history = laplace_gauss_seidel(phi, fixed_mask=fixed_mask)
    else:
        raise ValueError('Error! Invalid solver choice')

print(f'Converged in {it} iteration')

plot_heatmap(phi, mode)
plot_quiver(phi)
animate_solution(history)


    


