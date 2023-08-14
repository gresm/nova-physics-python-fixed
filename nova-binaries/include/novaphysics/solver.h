/*

  This file is a part of the Nova Physics Engine
  project and distributed under the MIT license.

  Copyright © Kadir Aksoy
  https://github.com/kadir014/nova-physics

*/

#ifndef NOVAPHYSICS_SOLVER_H
#define NOVAPHYSICS_SOLVER_H

#include "novaphysics/internal.h"
#include "novaphysics/body.h"
#include "novaphysics/collision.h"
#include "novaphysics/resolution.h"
#include "novaphysics/constraint.h"


/**
 * @file solver.h
 * 
 * @brief Collision and constraint solver functions.
 */


/**
 * @brief This is for specifying the method to mix various coefficients (restitution, friction).
 * 
 * @param AVG (a + b) / 2
 * @param SQRT sqrt(a * b)
 * @param MIN min(a, b)
 * @param MAX max(a, b)
 */
typedef enum {
    nv_CoefficientMix_AVG,
    nv_CoefficientMix_SQRT,
    nv_CoefficientMix_MIN,
    nv_CoefficientMix_MAX
} nv_CoefficientMix;

/**
 * @brief Mix two coefficients.
 * 
 * @param a First value
 * @param b Second value
 * @param mix Mixing type
 * @return nv_float 
 */
static inline nv_float nv_mix_coefficients(nv_float a, nv_float b, nv_CoefficientMix mix) {
    switch (mix) {
        case nv_CoefficientMix_AVG:
            return (a + b) / 2.0;

        case nv_CoefficientMix_SQRT:
            return nv_sqrt(a * b);

        case nv_CoefficientMix_MIN:
            return nv_fmin(a, b);

        case nv_CoefficientMix_MAX:
            return nv_fmax(a, b);

        default:
            NV_ERROR("Unknown coefficient mixing function.");
            return 0.0;
    }
}


/**
 * @brief Prepare for solving.
 * 
 * @param space Space
 * @param res Collision resolution
 * @param inv_dt Inverse delta time (1/Δt)
 */
void nv_presolve_collision(
    struct nv_Space *space,
    nv_Resolution *res,
    nv_float inv_dt
);

/**
 * @brief Solve positions (pseudo-velocities).
 * 
 * @param res Collision resolution
 */
void nv_solve_position(nv_Resolution *res);

/**
 * @brief Solve velocities.
 * 
 * @param res Collision resolution
 */
void nv_solve_velocity(nv_Resolution *res);


/**
 * @brief Prepare for solving.
 * 
 * @param space Space
 * @param cons Constraintt
 * @param inv_dt Inverse delta time (1/Δt)
 */
void nv_presolve_constraint(
    struct nv_Space *space,
    nv_Constraint *cons,
    nv_float inv_dt
);

/**
 * @brief Solve constraint.
 * 
 * @param cons Constraint
 */
void nv_solve_constraint(nv_Constraint *cons);


/**
 * @brief Prepare for solving.
 * 
 * @param space Space
 * @param cons Constraint
 * @param inv_dt Inverse delta time (1/Δt)
 */
void nv_presolve_spring(
    struct nv_Space *space,
    nv_Constraint *cons,
    nv_float inv_dt
);

/**
 * @brief Solve spring constraint.
 * 
 * @param cons Constraint
 */
void nv_solve_spring(nv_Constraint *cons);


/**
 * @brief Prepare for solving.
 * 
 * @param space Space
 * @param cons Constraint
 * @param inv_dt Inverse delta time (1/Δt)
 */
void nv_presolve_distance_joint(
    struct nv_Space *space,
    nv_Constraint *cons,
    nv_float inv_dt
);

/**
 * @brief Solve distance constraint.
 * 
 * @param cons Constraint
 */
void nv_solve_distance_joint(nv_Constraint *cons);


#endif