import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.animation as animation
from src.fields import compute_electric_field

def plot_heatmap(phi, sim_type=None, mode=None):
    plt.imshow(phi, origin='lower', cmap='hot')
    plt.colorbar(label='Tempetature')
    if sim_type == 'heat':
        if mode == 'center_hot' or mode == 'circle_hot':
            plt.title('Poisson Equation Solution (2D) (∇·(k∇φ) = -S)')
        elif mode == 'top_hot' or mode == 'sinusoidal_hot':
            plt.title('Laplace Equation Solution (2D) (∇²φ = 0)')
        else:
            plt.title('Heat Distribution')
    elif sim_type ==  'cpu':
        plt.title('CPU cooling simulation (Anisotropic Poisson)')


    # plt.savefig('../plots/heatmap.png')
    plt.show()

def plot_quiver(phi):
    Ex, Ey = compute_electric_field(phi)
    x = np.arange(1, phi.shape[0]-1)
    y = np.arange(1, phi.shape[1]-1)
    X, Y = np.meshgrid(x,y, indexing='ij')
    plt.imshow(phi, origin='lower', cmap='hot')
    plt.quiver(Y, X, Ey, Ex, color='white')
    plt.title('Electric Field from Potential')
    # plt.savefig('../plots/vectorFields.png')
    plt.show()

def animate_solution(history):

    vmax = max(np.max(frame) for frame in history)
    vmin = min(np.min(frame) for frame in history)

    fig, ax = plt.subplots(figsize=(8, 5))
    img = ax.imshow(history[0], cmap='hot', origin='lower', vmax=vmax, vmin=vmin)
    
    def update(frame):
        img.set_array(history[frame])
        ax.set_title(f'Iteration {frame}')
        return [img]

    ani = animation.FuncAnimation(
            fig, update, frames=len(history), interval=100, blit=True
            )
    
    # ani.save('../plots/poisson_animation.gif', writer='pillow', fps=10, dpi=150)
    plt.show()



