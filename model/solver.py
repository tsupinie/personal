
import numpy as np

def _buildCoeffArray(size, on_diag, off_diag):
    u_diag = np.diag(np.array([ off_diag ]).repeat(size - 1), k=1)
    c_diag = np.diag(np.array([ on_diag  ]).repeat(size))
    l_diag = np.diag(np.array([ off_diag ]).repeat(size - 1), k=-1)

    return u_diag + c_diag + l_diag

def diffusionEq(formulation='explicit'):
    def diffusionEqExplicit(u, discrete, thermal_conductivity):
        dx, dt = discrete
        return thermal_conductivity * np.gradient(np.gradient(u)) / dx ** 2

    def diffusionEqImplicit(u, discrete, thermal_conductivity):
        dx, dt = discrete
        lambda_factor = thermal_conductivity * dt / dx ** 2
        return _buildCoeffArray(len(u), 1 + 2 * lambda_factor, -lambda_factor)

    def diffusionEqCrankNicolson(u, discrete, thermal_conductivity):
        dx, dt = discrete
        lambda_factor = thermal_conductivity * dt / dx ** 2
        lhs_coeffs = _buildCoeffArray(len(u), 2 * (1 + lambda_factor), -lambda_factor)
        rhs_coeffs = _buildCoeffArray(len(u), 2 * (1 - lambda_factor), lambda_factor)
        return np.dot(np.linalg.inv(rhs_coeffs), lhs_coeffs)

    eq_formulations = { 'explicit':diffusionEqExplicit, 'implicit':diffusionEqImplicit, 'crankNicolson':diffusionEqCrankNicolson }

    return eq_formulations[formulation]

def eulerMethod(u, func, const, discrete):
    dx, dt = discrete
    return u + dt * func('explicit')(u, discrete, const)

def eulerBackwardMethod(u, func, const, discrete):
    dx, dt = discrete
    u_star = u + dt * func('explicit')(u, discrete, const)
    return u + dt * func('explicit')(u_star, discrete, const)

def implicitMethod(u, func, const, discrete):
    coeffs = func('implicit')(u, discrete, const)
    return np.linalg.solve(coeffs, u)

def crankNicolsonMethod(u, func, const, discrete):
    coeffs = func('crankNicolson')(u, discrete, const)
    return np.linalg.solve(coeffs, u)

def solve(u, func, method, const, bc, discrete):
    lbc, rbc = bc

    u[0] = lbc
    u[-1] = rbc

    iterations = 0
    while u[u.shape[0] / 2] < 71.1:
        if not (iterations % 10000): print "%f s: %f C" % (iterations * discrete[1], u[u.shape[0] / 2])
        # Find new solution
        u = method(u, func, const, discrete)
        # Apply boundary conditions
        u[0] = lbc
        u[-1] = rbc

        iterations += 1

    print "%f s" % (iterations * discrete[1])
    print u

    return

if __name__ == "__main__":
    nx = 101
    quad_init_cond = np.array([ -.25 * x ** 2 + 5 * x for x in range(nx) ])
    const_init_cond = np.array([ 21.0 for x in range(nx) ])

    # Thermal diffusivity = (Thermal conductivity) / (Density * Specific Heat at Constant Pressure) 
    const_wood = 0.22 / (2000 * 740)
    const_chicken = 0.476 / (3400 * 591.75)
    const_cookie = 0.405 / (3128 * 1252.3)

    solve(const_init_cond, diffusionEq, crankNicolsonMethod, const_cookie, (82., 82.), (0.03 / nx, 0.01))
