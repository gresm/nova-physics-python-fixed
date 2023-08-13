/*

  This file is a part of the Nova Physics Engine
  project and distributed under the MIT license.

  Copyright © Kadir Aksoy
  https://github.com/kadir014/nova-physics

*/

#ifndef NOVAPHYSICS_H
#define NOVAPHYSICS_H


/**
 * @file novaphysics.h
 * 
 * Main Nova Physics API
 */


// Stringify macro
#define _NV_STRINGIFY(x) #x
#define NV_STRINGIFY(x) _NV_STRINGIFY(x)

// Version in MAJOR.MINOR.PATCH format
#define NV_VERSION_MAJOR 0
#define NV_VERSION_MINOR 4
#define NV_VERSION_PATCH 0
// Version string
#define NV_VERSTR                          \
        NV_STRINGIFY(NV_VERSION_MAJOR) "." \
        NV_STRINGIFY(NV_VERSION_MINOR) "." \
        NV_STRINGIFY(NV_VERSION_PATCH)


#include "novaphysics/internal.h"

#include "novaphysics/vector.h"
#include "novaphysics/math.h"
#include "novaphysics/aabb.h"
#include "novaphysics/array.h"
#include "novaphysics/constants.h"
#include "novaphysics/material.h"

#include "novaphysics/space.h"
#include "novaphysics/body.h"
#include "novaphysics/constraint.h"
#include "novaphysics/collision.h"
#include "novaphysics/contact.h"
#include "novaphysics/solver.h"
#include "novaphysics/resolution.h"

#include "novaphysics/debug.h"


#endif