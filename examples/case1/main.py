import numpy as np

import sys; sys.path.insert(0, "../../src/")
from forchheimer import Forchheimer

sys.path.insert(0, "../common/")
import common

# In this test case we validate the MoLDD scheme for the Forchheimer model

# ------------------------------------------------------------------------------#

def test_mesh_size():

    end_time = 1
    num_steps = 5
    time_step = end_time / num_steps

    # the flow problem
    param = {
        "tol": 1e-6,
        "k": 1,
        "aperture": 1e-2, "kf_t": 1e2, "kf_n": 1e2,
        "mass_weight": 1.0/time_step, # inverse of the time step
        "num_steps": num_steps,
        "L": 1,  # l-scheme constant
        "beta": 1,
    }

    # loop over the mesh sizes
    mesh_sizes = np.array([0.5, 0.125, 0.03125])
    num_iter = np.empty((mesh_sizes.size, num_steps))

    for idx, mesh_size in enumerate(mesh_sizes):
        # solve the MoLDD scheme
        num_iter[idx, :]  = common.solve_MoLDD(mesh_size, param, Forchheimer)

    np.savetxt("forchheimer_mesh_size.txt", num_iter, fmt="%d", delimiter=",")

# ------------------------------------------------------------------------------#

def test_time_step():

    mesh_size = 0.125
    end_time = 1

    # the flow problem
    param = {
        "tol": 1e-6,
        "k": 1,
        "aperture": 1e-2, "kf_t": 1e2, "kf_n": 1e2,
        "L": 1,  # l-scheme constant
        "beta": 1,
    }

    # loop over the time steps
    num_steps = np.array([4, 8, 16])
    num_iter = np.zeros((num_steps.size, np.amax(num_steps)), dtype=np.int)

    for idx, num_step in enumerate(num_steps):
        time_step = end_time / num_step

        # consider the extra parameters
        param["mass_weight"] = 1.0/time_step
        param["num_steps"] = num_step

        # solve the MoLDD scheme
        num_iter[idx, :num_step] = common.solve_MoLDD(mesh_size, param, Forchheimer)

    np.savetxt("forchheimer_time_step.txt", num_iter, fmt="%d", delimiter=",")

# ------------------------------------------------------------------------------#

def test_parameters():

    mesh_size = 0.125

    end_time = 1
    num_steps = 5
    time_step = end_time / num_steps

    # the flow problem
    param = {
        "tol": 1e-6,
        "k": 1,
        "aperture": 1e-2, "kf_t": 1e2, "kf_n": 1e2,
        "mass_weight": 1.0/time_step, # inverse of the time step
        "num_steps": num_steps,
        "L": 1,  # l-scheme constant
    }

    # change the value of beta
    betas = np.array([1e-1, 1, 1e2])
    num_iter_beta = np.empty((betas.size, num_steps), dtype=np.int)
    for idx, beta in enumerate(betas):
        # consider the parameters
        param["beta"] = beta

        # solve the MoLDD scheme
        num_iter_beta[idx, :] = common.solve_MoLDD(mesh_size, param, Forchheimer)

    np.savetxt("forchheimer_beta_dependency.txt", num_iter_beta, fmt="%d", delimiter=",")

# ------------------------------------------------------------------------------#

def test_L():
    mesh_size = 0.125

    end_time = 1
    num_steps = 5
    time_step = end_time / num_steps

    # the flow problem
    param = {
        "tol": 1e-6,
        "k": 1,
        "aperture": 1e-2, "kf_t": 1e2, "kf_n": 1e2,
        "mass_weight": 1.0/time_step, # inverse of the time step
        "num_steps": num_steps,
        "beta": 50,
    }

    Ls = 0.025*np.arange(101)
    num_iter_L = np.empty((Ls.size, num_steps), dtype=np.int)
    for idx, L in enumerate(Ls):
        param["L"] = L

        # solve the MoLDD scheme
        num_iter_L[idx, :] = common.solve_MoLDD(mesh_size, param, Forchheimer)

    np.savetxt("forchheimer_L_dependency.txt", num_iter_L, fmt="%d", delimiter=",")

# ------------------------------------------------------------------------------#

def main():

    h = 0.125

    end_time = 1
    num_steps = 5
    time_step = end_time / num_steps

    # the flow problem
    param = {
        "tol": 1e-6,
        "k": 1,
        "aperture": 1e-2, "kf_t": 1e2, "kf_n": 1e2,
        "mass_weight": 1.0/time_step, # inverse of the time step
        "num_steps": num_steps,
        "L": 1e0,  # l-scheme constant
        "beta": 1e2,  # non-linearity constant
    }

    # solve the MoLDD scheme
    num_iter = common.solve_MoLDD(h, param, Forchheimer)

    print(num_iter)

# ------------------------------------------------------------------------------#

if __name__ == "__main__":
    #test_mesh_size()
    #test_time_step()
    test_parameters()
    #test_L()
    #main()
