import numpy as np

def laplace_jacobi(phi, max_iter=10000, tol=1e-5, 
                   interval=50, fixed_mask=None):
    new_phi = phi.copy()
    history = []

    for it in range(max_iter):
        old_phi = new_phi.copy()
        new_phi[1:-1, 1:-1] = 0.25 * (
            old_phi[2:, 1:-1] + old_phi[:-2, 1:-1] +
            old_phi[1:-1, 2:] + old_phi[1:-1, :-2]
        )

        if fixed_mask is not None:
            new_phi[fixed_mask] = phi[fixed_mask]

        if it % interval == 0:
            history.append(new_phi.copy())

        diff = np.max(np.abs(new_phi - old_phi))
        if diff < tol:
            break

    history.append(new_phi.copy())
    return it, new_phi, history


def laplace_gauss_seidel(phi, max_iter=10000, tol=1e-5, 
                         save_interval=50, fixed_mask=None):
    history = []
    for it in range(max_iter):
        old_phi = phi.copy()

        for i in range(1, phi.shape[0] - 1):
            for j in range(1, phi.shape[1] - 1):
                if fixed_mask is not None and fixed_mask[i, j]:
                    continue
                phi[i, j] = 0.25 * (
                    phi[i+1, j] + phi[i-1, j] +
                    phi[i, j+1] + phi[i, j-1]
                )
        if fixed_mask is not None:
            phi[fixed_mask] = old_phi[fixed_mask]

        if it % save_interval == 0:
            history.append(phi.copy())

        diff = np.max(np.abs(phi - old_phi))
        if diff < tol:
            break

    history.append(phi.copy())
    return it, phi, history

def poisson_jacobi(phi, source_term, max_iter=10000, 
                   tol=1e-5, save_interval=50, fixed_mask=None):
    history = []
    new_phi = phi.copy()
    h2 = 1.0

    for it in range(max_iter):
        old_phi = new_phi.copy()
        new_phi[1:-1, 1:-1] = 0.25 * (
                old_phi[2:, 1:-1] + old_phi[:-2,1:-1] + 
                old_phi[1:-1, 2:] + old_phi[1:-1, :-2] - 
                h2 * source_term[1:-1, 1:-1]
                ) 
        if fixed_mask is not None:
            new_phi[fixed_mask] = phi[fixed_mask]

        if it % save_interval == 0:
            history.append(new_phi.copy())

        diff = np.max(np.abs(new_phi - old_phi))    
        if diff < tol:
            break

    history.append(new_phi.copy())
    return it, new_phi, history

def poisson_gauss_seidel(phi, source_term, max_iter=10000, 
                         tol=1e-5, save_interval=50, fixed_mask=None):
    history = []
    h2 = 1.0


    for it in range(max_iter):
        old_phi = phi.copy()
        for i in range(1, phi.shape[0] - 1):
            for j in range(1, phi.shape[1] - 1):
                if fixed_mask is not None and fixed_mask[i, j]:
                    continue

                phi[i,j] = 0.25 * (
                        phi[i+1,j] + phi[i-1, j] + 
                        phi[i, j+1] + phi[i, j-1] - 
                        h2 * source_term[i, j] 
                                   )

        if fixed_mask is not None:
            phi[fixed_mask] = old_phi[fixed_mask]

        if it % save_interval == 0:
            history.append(phi.copy())
        
        diff = np.max(np.abs(phi - old_phi))
        if diff < tol:
            break
    
    history.append(phi.copy())
    return it, phi, history
