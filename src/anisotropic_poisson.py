import numpy as np 

def anisotropic_poisson_solver(phi, source, k, fixed_mask, max_iter=5000, tol=1e-5):
    
    history = []
    for it in range(max_iter):
        old_phi = phi.copy()

        for i in range(1, phi.shape[0]-1):
            for j in range(1, phi.shape[1]-1):
                if fixed_mask[i,j]:
                    continue

                k_e = 0.5 * (k[i,j] + k[i+1, j]) # East (right)
                k_w = 0.5 * (k[i,j] + k[i-1, j]) # West (left)
                k_n = 0.5 * (k[i,j] + k[i, j+1]) # North (up) 
                k_s = 0.5 * (k[i,j] + k[i, j-1]) # South (down)

                numerator = (
                        k_e * phi[i+1, j] + k_w * phi[i-1, j] + 
                        k_n * phi[i, j+1] + k_s * phi[i, j-1] - 
                        source[i,j]
                        )

                denominator = k_e + k_w + k_n + k_s

                if denominator == 0:
                    continue

                phi[i,j] = numerator / denominator
                
        if it % 10 == 0:
            history.append(phi.copy())

        diff = np.max(np.abs(old_phi - phi))
        if diff < tol:
            break

    return it, phi, history







