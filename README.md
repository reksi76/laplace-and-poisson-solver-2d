# laplace-solver-2d

Numerical solution of the **Laplace equation** using **Jacobi** and **Gauss Seidel** method


## Mathematical background

# The 2D Laplace equation

[

nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} = 0

]


# Finite difference discretization:

[

phi\_{i,j} = \frac{1}{4} \bigl( \phi\_{i+1,j} + \phi\_{i-1,j} + \phi\_{i,j+1} + \phi\_{i,j-1} \bigr)

]


## Example result (top_hot)


# Heat map

![Heat map](plots/heatmap.png)

# vector field

![vector field](plots/vectorFields.png)

# Animation

![Heat map animation](/plots/animation.gif)


The solver currently supports several boundary condition modes:

- top_hot – The top boundary of the plate is heated while other sides are kept at zero temperature.

- center_hot – A single hot point is placed at the center of the plate.

- circle_hot – A circular hot region is placed at the center.

- sinusoidal_hot – A sinusoidal temperature profile is applied along the top boundary.
