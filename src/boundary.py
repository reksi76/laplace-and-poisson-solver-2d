import numpy as np
from anisotropic_poisson import anisotropic_poisson_solver

V0 = 100.0
def set_plate_bc(nx, ny, mode = 'top_hot'):
    phi = np.zeros((nx, ny))
    fixed_mask = np.zeros_like(phi, dtype=bool)
    source_term = np.zeros_like(phi)
    
    if mode == 'top_hot':
        phi[-1,:] = V0

    elif mode == 'center_hot':
        cx, cy = nx // 2, ny // 2
        r = min(cx, cy) // 4

        y, x = np.ogrid[:nx, :ny]
        mask_center = (x - cx)**2 + (y - cy)**2 <= r**2
        phi[mask_center] = V0

        phi[0, :] = phi[-1, :] = 20.0
        phi[:, 0] = phi[:, -1] = 20.0
        fixed_mask[0, :] = fixed_mask[-1, :] = True
        fixed_mask[:, 0] = fixed_mask[:, -1] = True

        source_term[mask_center] = -5.0
    
    elif mode == 'sinusoidal_hot':
        x = np.linspace(0, 2*np.pi, ny)
        phi[0,:] = 50 + 50 * np.sin(x)
        fixed_mask[0, :] = True

    elif mode == 'circle_hot':
        cx, cy = nx // 2, ny // 2
        r = min(nx, ny) // 6  

        y, x = np.ogrid[:nx, :ny]

        circle_mask = (x - cx)**2 + (y - cy)**2 <= r**2


        phi[0, :] = phi[-1, :] = 20.0
        phi[:, 0] = phi[:, -1] = 20.0
        fixed_mask[0, :] = fixed_mask[-1, :] = True
        fixed_mask[:, 0] = fixed_mask[:, -1] = True

        source_term[circle_mask] = -5.0    
        print(f"[DEBUG] mode={mode} | source sum={np.sum(source_term):.2f} | fixed={np.sum(fixed_mask)}")

    return phi, fixed_mask, source_term

def cpu_cooling_simulation(nx, ny):
    phi = np.zeros((nx, ny))
    fixed_mask = np.zeros_like(phi, dtype=bool)
    source_term = np.zeros_like(phi)

    die_x, die_y = nx//2, ny//2 
    die_size = 5 
    die_area = (slice(die_x - die_size, die_x + die_size), 
                slice(die_y - die_size, die_y + die_size))

    source_term[die_area] = 100.0
    fixed_mask[die_area] = True
    phi[die_area] = 85.0

    # heat sink base
    phi[0, :] = 25.0
    fixed_mask[0, :] = True

    # Heat pipes

    thermal_conductivity = np.ones((nx, ny))
    hot_pipe_location = [
            (slice(20, 80), slice(ny//2-2, ny//2+2)),
            (slice(nx//2-2, nx//2+2), slice(20,80))
            ]
    for area in hot_pipe_location:
        thermal_conductivity[area] = 5.0

    print('CPU cooling simulation...')
    it, result, history = anisotropic_poisson_solver(
            phi, source_term, thermal_conductivity, fixed_mask=fixed_mask
            )

    return it, result, history




