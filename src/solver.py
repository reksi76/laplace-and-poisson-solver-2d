import numpy as np

def laplace_jacobi(phi, max_iter=10000, tol=1e-5, interval=50, fixed_mask=None):
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

    return it, new_phi, history


def laplace_gauss_seidle(phi, max_iter=10000, tol=1e-5, save_interval=50, fixed_mask=None):
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

        if it % save_interval == 0:
            history.append(phi.copy())

        diff = np.max(np.abs(phi - old_phi))
        if diff < tol:
            break

    return it, phi, history
