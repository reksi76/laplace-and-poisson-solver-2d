import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import numpy as np 
from boundary import set_plate_bc, cpu_cooling_simulation
from visualize import plot_heatmap, plot_quiver, animate_solution 
from solver import laplace_jacobi, laplace_gauss_seidel, poisson_jacobi, poisson_gauss_seidel
from anisotropic_poisson import anisotropic_poisson_solver

parser = argparse.ArgumentParser(description='2D Laplace Equation Solver')
subparser = parser. add_subparsers(dest='sim', help='Choose simulation')

heat_parser = subparser.add_parser('heat', help='2D Heat Diffusion')
heat_parser.add_argument(
        '--solver', choices=['jacobi', 'gauss'], default='gauss', 
        help='choose a solver method (gauss or jacobi)'
        )
heat_parser.add_argument(
        '--mode', choices=['top_hot', 'center_hot', 'sinusoidal_hot', 'circle_hot'], 
        default='top_hot', help='Boundary mode (top_hot, center_hot, sinusoidal_hot, circle_hot)')
heat_parser.add_argument(
        '--nx', type=int, default=50, help='Number of grid x'
        )
heat_parser.add_argument(
        '--ny', type=int, default=50, help='Number of grid y'
        )

cpu_parser = subparser.add_parser(
        'cpu', help='CPU Cooling Simulation'
        )
cpu_parser.add_argument(
        '--nx', type=int, default=50, help='Number of Grid x'
        )
cpu_parser.add_argument(
        '--ny', type=int, default=50, help= 'Number of Grid y'
        )

args = parser.parse_args()

if args.sim == 'heat':
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

if args.sim == 'cpu':
    print('Processing CPU cooling simulation...')
    it, result, history = cpu_cooling_simulation(args.nx, args.ny)


print(f'Converged in {it} iterations')
if args.sim == 'heat':
    plot_heatmap(phi, args.sim, args.mode)
    plot_quiver(phi)
else:
    plot_heatmap(result, args.sim)

animate_solution(history)

