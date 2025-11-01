import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np 
from boundary import set_plate_bc
from visualize import plot_heatmap, plot_quiver, animate_solution 
from solver import laplace_jacobi, laplace_gauss_seidel, poisson_jacobi, poisson_gauss_seidel

parser = argparse.ArgumentParser(description='2D Laplace Equation Solver')
parser.add_argument('--solver', choices=['jacobi', 'gauss'], default='gauss', help='choose a solver method (gauss or jacobi)')
parser.add_argument('--mode', choices=['top_hot', 'center_hot', 'sinusoidal_hot', 'circle_hot'], default='top_hot', help='Boundary mode (top_hot, center_hot, sinusoidal_hot, circle_hot)')
parser.add_argument('--nx', type=int, default=50, help='Number of grid x')
parser.add_argument('--ny', type=int, default=50, help='Number of grid y')

args = parser.parse_args()
phi, fixed_mask, source_term = set_plate_bc(args.nx, args.ny, args.mode)

poisson_mode = ['center_hot', 'circle_hot']

if args.mode in poisson_mode:
    print(f'Using poisson equation for {args.mode} (internal heat source)')
    if args.solver == 'jacobi':
        it, phi, history = poisson_jacobi(phi, source_term, fixed_mask=fixed_mask)
    else:
        it, phi, history = poisson_gauss_seidel(phi, source_term, fixed_mask=fixed_mask)
else:
    print(f'Using laplace equation for {args.mode} (boundary heat only)')
    if args.solver == 'jacobi':
        it, phi, history = laplace_jacobi(phi, fixed_mask=fixed_mask)
    else:
        it, phi, history = laplace_gauss_seidel(phi, fixed_mask=fixed_mask)

print(f'Converged in {it} iterations')
plot_heatmap(phi, args.mode)
plot_quiver(phi)
animate_solution(history)

