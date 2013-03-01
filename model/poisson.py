
import numpy as np

###############################################
# poisson.py
# Author: Tim Supinie (tsupinie@ou.edu)
# February 2012
###############################################

def laplacian(grid, boundaries, grid_spacing=1):
    grid_x0 = np.zeros(grid.shape)
    grid_x2 = np.zeros(grid.shape)
    grid_y0 = np.zeros(grid.shape)
    grid_y2 = np.zeros(grid.shape)

    boundary_y1, boundary_y2, boundary_x1, boundary_x2 = boundaries

    # Set the grid for G_{i,j-1}
    grid_x0[0, :] = boundary_x1
    grid_x0[1:, :] = grid[:-1, :]

    # Set the grid for G_{i,j+1}
    grid_x2[-1, :] = boundary_x2
    grid_x2[:-1, :] = grid[1:, :]

    # Set the grid for G_{i-1,j}
    grid_y0[:, 0] = boundary_y1
    grid_y0[:, 1:] = grid[:, :-1]

    # Set the grid for G_{i+1,j}
    grid_y2[:, -1] = boundary_y2
    grid_y2[:, :-1] = grid[:, 1:]

    return (grid_x0 + grid_x2 + grid_y0 + grid_y2 - 4 * grid) / grid_spacing ** 2

def poisson_solve(grid, forcing, boundaries, grid_spacing=1):
    """
    poisson_solve()
    Purpose:    Solves an equation of the form laplacian(x) = f for x given boundary conditions
                    and forcing using the relaxation method.  Method from Alan Shapiro via Greg 
                    Blumberg (2012, personal communication).
    Parameters: grid [type=np.ndarray]
                    Initial grid to use in the iteration.  An array full of 0's should be fine.
                forcing [type=np.ndarray]
                    Array containing the forcing term for the equation.
                boundaries [type=tuple,list]
                    A list or tuple containing the boundary conditions in the following order: 
                    southern, northern, western, eastern.
    Returns:    The solved grid.
    """

    # Initialize variables
    residual = 0
    while type(residual) == int or np.abs(residual).sum() > 1e-8:
    
        # Compute the residual
        residual = laplacian(grid, boundaries, grid_spacing) - forcing

        # Update the guess
        grid += residual * grid_spacing ** 2 / 4.

    return grid

def main():
    # Test code ...
    grid_x = 50
    grid_y = 60

    grid = np.zeros((grid_x, grid_y))
    xs, ys = np.meshgrid(np.arange(grid_y), np.arange(grid_x))
    forcing = np.exp(-2 * ((xs - grid_x / 2) ** 2 + (ys - grid_y / 2) ** 2) / min(grid_x, grid_y))

    boundary = (10 * np.ones(grid_x), 10 * np.ones(grid_x), 10 * np.ones(grid_y), 10 * np.ones(grid_y))
    grid = poisson_solve(grid, forcing, boundary)

    print (laplacian(grid, boundary) - forcing).sum()

    return

if __name__ == "__main__":
    main()
