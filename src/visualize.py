import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.animation as animation
from src.fields import compute_electric_field

def plot_heatmap(phi):
    plt.imshow(phi, origin='lower', cmap='hot')
    plt.colorbar(label='Tempetature')
    plt.title('Laplace Equation Solution (2D)')
    plt.show()

def plot_quiver(phi):
    Ex, Ey = compute_electric_field(phi)
    x = np.arange(1, phi.shape[0]-1)
    y = np.arange(1, phi.shape[1]-1)
    X, Y = np.meshgrid(x,y, indexing='ij')
    plt.imshow(phi, origin='lower', cmap='hot')
    plt.quiver(Y, X, Ey, Ex, color='white')
    plt.title('Electric Field from Potential')
    plt.show()

def animate_solution(history):
    fig, ax = plt.subplots(figsize=(8, 5))
    img = ax.imshow(history[0], cmap='inferno', origin='lower')

    def update(frame):
        img.set_array(history[frame])
        ax.set_title(f'Iteration {frame}')
        return [img]

    ani = animation.FuncAnimation(
            fig, update, frames=len(history), interval=100, blit=True
            )
    
    ani.save('../plots/animation.gif', writer='pillow', fps=10, dpi=150)
    plt.show()



