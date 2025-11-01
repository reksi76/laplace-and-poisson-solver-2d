import numpy as np 

V0 = 100.0
def set_plate_bc(nx, ny, mode = 'top_hot'):
    phi = np.zeros((nx, ny))
    fixed_mask = np.zeros_like(phi, dtype=bool)
    source_term = np.zeros_like(phi)
    
    if mode == 'top_hot':
        phi[-1,:] = V0
        # fixed_mask = True

    elif mode == 'center_hot':
        cx, cy = nx // 2, ny // 2
        r = min(cx, cy) // 4

        y, x = np.ogrid[:nx, :ny]
        mask_center = (x - cx)**2 + (y - cy)**2 <= r**2
        phi[mask_center] = V0
        fixed_mask[mask_center] = True

        phi[0, :] = phi[-1, :] = 20.0
        phi[:, 0] = phi[:, -1] = 20.0
        fixed_mask[0, :] = fixed_mask[-1, :] = True
        fixed_mask[:, 0] = fixed_mask[:, -1] = True

        source_term[:] = 0
    
    elif mode == 'sinusoidal_hot':
        x = np.linspace(0, 2*np.pi, ny)
        phi[0,:] = 50 + 50 * np.sin(x)
        fixed_mask[0, :] = True

    elif mode == 'circle_hot':
        cx, cy = nx // 2, ny // 2
        r = min(nx, ny) // 6  

        y, x = np.ogrid[:nx, :ny]

        circle_mask = (x - cx)**2 + (y - cy)**2 <= r**2

        phi[circle_mask] = V0
        fixed_mask[circle_mask] = True

        phi[0, :] = phi[-1, :] = 20.0
        phi[:, 0] = phi[:, -1] = 20.0
        fixed_mask[0, :] = fixed_mask[-1, :] = True
        fixed_mask[:, 0] = fixed_mask[:, -1] = True

        source_term[:] = 0    
        print(f"[DEBUG] mode={mode} | source sum={np.sum(source_term):.2f} | fixed={np.sum(fixed_mask)}")

    return phi, fixed_mask, source_term
