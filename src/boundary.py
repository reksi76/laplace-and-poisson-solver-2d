import numpy as np 

V0 = 100.0
def set_plate_bc(nx, ny, mode = 'top_hot'):
    phi = np.zeros((nx, ny))
    fixed_mask = np.zeros_like(phi, dtype=bool)
    
    if mode == 'top_hot':
        phi[-1,:] = V0

    elif mode == 'center_hot':
        cx, cy = nx // 2, ny // 2
        phi[cx, cy] = V0   
        fixed_mask[cx, cy] = True

    
    elif mode == 'sinusoidal_hot':
        x = np.linspace(0, 2*np.pi, ny)
        phi[0,:] = 50 + 50 * np.sin(x)
        fixed_mask[0, :] = True

    elif mode == 'circle_hot':
        y, x = np.ogrid[:ny, :nx]
        cx, cy = nx // 2, ny // 2
        r = min(nx, ny) // 4
       
        distance_sq = (x - cx)**2 + (y - cy)**2
        circle_mask = distance_sq <= r**2
        phi[circle_mask] = V0 
        fixed_mask[circle_mask] = V0

    return phi, fixed_mask
