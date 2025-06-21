# test_solver.py - PyTest for CFD solver

import pytest
from cfd import solve_flow
import numpy as np

@pytest.mark.parametrize("nx, ny, nu, u_in, p_out, n_steps, expected_mean_u", [
    (50, 50, 1e-3, 1.0, 0.0, 2000, 0.02)
])
def test_baseline_case(nx, ny, nu, u_in, p_out, n_steps, expected_mean_u):
    result = solve_flow(nx, ny, nu, u_in, p_out, n_steps)
    assert np.isclose(result['u'].mean(), expected_mean_u, atol=0.02)

def test_residual_convergence():
    result = solve_flow(50, 50, 1e-3, 1.0, 0.0, 400)
    assert result['max_residual'] < 1e-3

def test_edge_cases():
    # Small grid
    result_small = solve_flow(10, 10, 1e-3, 1.0, 0.0, 100)
    assert result_small is not None
    # Large grid
    result_large = solve_flow(200, 200, 1e-3, 1.0, 0.0, 100)
    assert result_large is not None