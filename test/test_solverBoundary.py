import os
import sys
import numpy as np 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.solver import laplace_jacobi, laplace_gauss_seidel, poisson_jacobi, poisson_gauss_seidel
    from src.boundary import set_plate_bc

except ImportError as e:
    print(f'Failed to import modules: {e}')
    exit(1)

def test_basic_functionality():
    print('Test 1: Basic Functionality')
    print('Testing boundary condition')
    for mode in ['top_hot', 'sinusoidal_hot', 'circle_hot', 'center_hot']:
        phi, fixed_mask, _ = set_plate_bc(10, 10, mode)
        print (f'   {mode}: phi shape {phi.shape}, fixed points:{np.sum(fixed_mask)}')

    print('Testing laplace solver')
    it, fixed_mask, _ = set_plate_bc(8, 8, 'top_hot')

    it_jb, phi_jb, hist_jb = laplace_jacobi(phi.copy(), max_iter=100, tol=1e-4)
    it_gs, phi_gs, hist_gs = laplace_gauss_seidel(phi.copy(), max_iter=100, tol=1e-4)

    print(f'    jacobi: {it_jb} iteration, history: {len(hist_jb)}')
    print(f'    gauss-seidel: {it_gs} iteration, history: {len(hist_gs)}')

    print('Testing poisson solver')
    phi, fixed_mask, source = set_plate_bc(8, 8, 'center_hot')
    source[4,4] = 1.0

    it_pj, phi_pj, hist_pj = poisson_jacobi(phi.copy(), source, max_iter=100, tol=1e-4)
    it_pgs, phi_pgs, hist_pgs = poisson_gauss_seidel(phi.copy(), source, max_iter=100, tol=1e-4)

    print(f'    Poisson jacobi: {it_pj} iterations')
    print(f'    Poisson gauss-seidel: {it_pgs} iterations')
    print('Basic functionality tests PASSED!')

def test_convergance():
    print('\nTest 2: Test Convergance')
    
    print('Laplace convergent test')
    phi, fixed_mask, _= set_plate_bc(10, 10, 'top_hot')

    it_jb, phi_jb, hist_jb = laplace_jacobi(phi.copy(), max_iter=1000, tol=1e-4)
    assert it_jb < 1000, f'Jacobi is not convergent in {it_jb} iteration'
    print(f'Jacobi convergent in {it_jb} iterations')

    it_gs, phi_gs, _ = laplace_gauss_seidel(phi.copy(), max_iter=1000, tol=1e-4)
    assert it_gs < 1000, f'Gaussian is not convergent in {it_gs} iteration'
    print(f'Gauss-Seidel convergent in {it_gs} iterations')

    print('Convergent test PASSED!')

def test_boundary():
    print('\nTest 3: Boundary')
    
    # Jacobi boundary test
    phi, fixed_mask, _ = set_plate_bc(12, 12, 'top_hot')
    original_boundary = phi[-1, :].copy()

    it_jb, phi_jb, _ = laplace_jacobi(phi.copy(), max_iter=200, tol=1e-4)

    assert np.allclose(original_boundary, phi_jb[-1, :]), 'Top boundary changed'
    print('    Boundary values preserved in jacobi')

    # Gauss seidel boundary test
    phi, fixed_mask, _ = set_plate_bc(12, 12, 'top_hot')
    original_boundary = phi[-1, :].copy()

    it_gs, phi_gs, _ = laplace_gauss_seidel(phi.copy(), max_iter=200, tol=1e-4)

    assert np.allclose(original_boundary, phi_gs[-1,:].copy()), 'Top boundary changed'
    print('    Boundary values preserved in gauss-seidel')

    print('Boundary test for laplace equation PASSED')

def test_fixed_mask():
    print('\nTest 4: fixed Mask')
    
    # Fixed mask test for poisson_jacobi
    phi, fixed_mask, source = set_plate_bc(10, 10, 'center_hot')
    original_fixed_values = phi[fixed_mask].copy()

    it_pj, phi_pj, _ = poisson_jacobi(phi.copy(),source, max_iter=200, tol=1e-4, fixed_mask=fixed_mask)

    assert np.allclose(original_fixed_values, phi_pj[fixed_mask]), 'Fixed mask points changed!'
    print(f'    {np.sum(fixed_mask)} fixed points preserved')

    # fixed mask test for poisson_gauss_seidel
    it_pgs, phi_pgs, source = poisson_gauss_seidel(phi.copy(), source, max_iter=200, tol=1e-4, fixed_mask=fixed_mask)

    assert np.allclose(original_fixed_values, phi_pj[fixed_mask]), 'Fixed mask points changed!'
    print(f'    {np.sum(fixed_mask)} fixed points preserved')

    print('Fixed mask test PASSED')

def test_np_crash():
    print('\nTEST 5: No crash with weird input')

    try:
        phi, fixed_mask, _ = set_plate_bc(3, 3, 'top_hot')
        it_jb, phi_jb, _ = laplace_jacobi(phi.copy(), max_iter=10, tol=1e-3)
        print('    Small grid(3x3) - OK')

    except exception as e:
        print(f'    Small grid failed: {e}')

    try:
        phi, fixed_mask, _ = set_plate_bc(8, 8, 'top_hot')
        it_jb, phi_jb, _ = laplace_jacobi(phi.copy(), max_iter=50, tol=1e-10)
        print('    Strict tolerance - OK')
    
    except exception as e:
        print(f'    Strict tolerance failed: {e}')

    print('Test 5 PASSED')

def run_all_test():
    print('SOLVER TEST SUITE')
    print('=' * 50)

    tests = [test_basic_functionality,
            test_convergance,
            test_boundary,
            test_fixed_mask,
            test_np_crash]

    passsed = 0 
    total = len(test)

    for test in tests:
        try:
            test()
            passed += 1 

        except exception as e:
            print(f'{test.__name__} failed: {e}')

    print('=' * 50)
    print(f'Result: {passed}/{total} tests passed')

    if passed == total:
        print('ALL TEST PASSED!')
    else:
        print(f'{total - passed} tests failed')

    return passed == total

if __name__ == '__main__':
    success = run_all_test()
    exit(0 if success else 1)

            



        

    




