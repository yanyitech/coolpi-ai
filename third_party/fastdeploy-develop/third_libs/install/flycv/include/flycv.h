// Copyright (c) 2022 FlyCV Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include "flycv_namespace.h"

/* core module */
#define BUILD_FCV_CORE
#define WITH_FCV_BASE
#define WITH_FCV_MAT
#define WITH_FCV_ALLOCATOR
#define WITH_FCV_BASIC_MATH
#define WITH_FCV_PARALLEL
#define WITH_FCV_CPU
/* #undef WITH_FCV_OPENCL */

/* img_transform module */
#define BUILD_FCV_IMG_TRANSFORM
#define WITH_FCV_COLOR_CONVERT
#define WITH_FCV_RESIZE
#define WITH_FCV_WARP_AFFINE
#define WITH_FCV_WARP_PERSPECTIVE
#define WITH_FCV_ROTATION
#define WITH_FCV_FLIP
#define WITH_FCV_SUBTRACT
#define WITH_FCV_COPY_MAKE_BORDER
#define WITH_FCV_CROP
#define WITH_FCV_REMAP
#define WITH_FCV_ADD_WEIGHTED
#define WITH_FCV_EXTRACT_CHANNEL

/* img_calculation module */
#define BUILD_FCV_IMG_CALCULATION
#define WITH_FCV_MATRIX_MUL
#define WITH_FCV_NORM
#define WITH_FCV_MEAN
#define WITH_FCV_MIN_AREA_RECT
#define WITH_FCV_MIN_MAX_LOC
#define WITH_FCV_CONNECTED_COMPONENTS
#define WITH_FCV_FIND_HOMOGRAPHY

/* fusion_api module */
#define BUILD_FCV_FUSION_API
#define WITH_FCV_BGR_TO_RGBA_WITH_MASK
#define WITH_FCV_NORMALIZE_TO_SUBMEAN_TO_REORDER
#define WITH_FCV_SPLIT_TO_MEMCPY
#define WITH_FCV_Y420SP_TO_RESIZE_TO_BGR
#define WITH_FCV_BGRA_TO_RESIZE_TO_BGR

/* math_operator module */
#define BUILD_FCV_MATH_OPERATOR
#define WITH_FCV_VECTOR_OPERATOR

/* media_io module */
#define BUILD_FCV_MEDIA_IO
#define WITH_FCV_IMGCODECS

/* img_draw module */
#define BUILD_FCV_IMG_DRAW
#define WITH_FCV_FILL_POLY
#define WITH_FCV_POLY_LINES
#define WITH_FCV_CIRCLE
#define WITH_FCV_LINE

/* core module header file reference */
#ifdef BUILD_FCV_CORE
#ifdef WITH_FCV_BASE
#include "modules/core/base/interface/macro_export.h"
#include "modules/core/base/interface/log.h"
#include "modules/core/base/interface/basic_types.h"
#include "modules/core/base/interface/macro_ns.h"
#endif
#ifdef WITH_FCV_MAT
#include "modules/core/mat/interface/mat.h"
#endif
#ifdef WITH_FCV_ALLOCATOR
#include "modules/core/allocator/interface/base_allocator.h"
#endif
#ifdef WITH_FCV_BASIC_MATH
#include "modules/core/basic_math/interface/basic_math.h"
#endif
#ifdef WITH_FCV_PARALLEL
#include "modules/core/parallel/interface/parallel.h"
#endif
#ifdef WITH_FCV_CPU
#include "modules/core/cpu/interface/cpu.h"
#endif
#ifdef WITH_FCV_OPENCL
#include "modules/core/opencl/interface/opencl.h"
#endif
#endif

/* img_transform module header file reference */
#ifdef BUILD_FCV_IMG_TRANSFORM
#ifdef WITH_FCV_COLOR_CONVERT
#include "modules/img_transform/color_convert/interface/color_convert.h"
#endif
#ifdef WITH_FCV_RESIZE
#include "modules/img_transform/resize/interface/resize.h"
#endif
#ifdef WITH_FCV_WARP_AFFINE
#include "modules/img_transform/warp_affine/interface/warp_affine.h"
#endif
#ifdef WITH_FCV_WARP_PERSPECTIVE
#include "modules/img_transform/warp_perspective/interface/warp_perspective.h"
#endif
#ifdef WITH_FCV_ROTATION
#include "modules/img_transform/rotation/interface/rotation.h"
#endif
#ifdef WITH_FCV_FLIP
#include "modules/img_transform/flip/interface/flip.h"
#endif
#ifdef WITH_FCV_SUBTRACT
#include "modules/img_transform/subtract/interface/subtract.h"
#endif
#ifdef WITH_FCV_COPY_MAKE_BORDER
#include "modules/img_transform/copy_make_border/interface/copy_make_border.h"
#endif
#ifdef WITH_FCV_CROP
#include "modules/img_transform/crop/interface/crop.h"
#endif
#ifdef WITH_FCV_REMAP
#include "modules/img_transform/remap/interface/remap.h"
#endif
#ifdef WITH_FCV_ADD_WEIGHTED
#include "modules/img_transform/add_weighted/interface/add_weighted.h"
#endif
#ifdef WITH_FCV_EXTRACT_CHANNEL
#include "modules/img_transform/extract_channel/interface/extract_channel.h"
#endif
#endif

/* img_calculation module header file reference */
#ifdef BUILD_FCV_IMG_CALCULATION
#ifdef WITH_FCV_MATRIX_MUL
#include "modules/img_calculation/matrix_mul/interface/matrix_mul.h"
#endif
#ifdef WITH_FCV_NORM
#include "modules/img_calculation/norm/interface/norm.h"
#endif
#ifdef WITH_FCV_MEAN
#include "modules/img_calculation/mean/interface/mean.h"
#endif
#ifdef WITH_FCV_MIN_AREA_RECT
#include "modules/img_calculation/min_area_rect/interface/min_area_rect.h"
#endif
#ifdef WITH_FCV_MIN_MAX_LOC
#include "modules/img_calculation/min_max_loc/interface/min_max_loc.h"
#endif
#ifdef WITH_FCV_CONNECTED_COMPONENTS
#include "modules/img_calculation/connected_components/interface/connected_components.h"
#endif
#ifdef WITH_FCV_FIND_HOMOGRAPHY
#include "modules/img_calculation/find_homography/interface/find_homography.h"
#endif
#endif

/* fusion_api module header file reference */
#ifdef BUILD_FCV_FUSION_API
#ifdef WITH_FCV_BGR_TO_RGBA_WITH_MASK
#include "modules/fusion_api/bgr_to_rgba_with_mask/interface/bgr_to_rgba_with_mask.h"
#endif
#ifdef WITH_FCV_NORMALIZE_TO_SUBMEAN_TO_REORDER
#include "modules/fusion_api/normalize_to_submean_to_reorder/interface/normalize_to_submean_to_reorder.h"
#endif
#ifdef WITH_FCV_SPLIT_TO_MEMCPY
#include "modules/fusion_api/split_to_memcpy/interface/split_to_memcpy.h"
#endif
#ifdef WITH_FCV_Y420SP_TO_RESIZE_TO_BGR
#include "modules/fusion_api/y420sp_to_resize_to_bgr/interface/y420sp_to_resize_to_bgr.h"
#endif
#ifdef WITH_FCV_BGRA_TO_RESIZE_TO_BGR
#include "modules/fusion_api/bgra_to_resize_to_bgr/interface/bgra_to_resize_to_bgr.h"
#endif
#endif

/* math_operator module header file reference */
#ifdef BUILD_FCV_MATH_OPERATOR
#ifdef WITH_FCV_VECTOR_OPERATOR
#include "modules/math_operator/vector_operator/interface/vector_operator.h"
#endif
#endif

/* media_io module header file reference */
#ifdef BUILD_FCV_MEDIA_IO
#ifdef WITH_FCV_IMGCODECS
#include "modules/media_io/imgcodecs/interface/imgcodecs.h"
#endif
#endif

/* img_draw module header file reference */
#ifdef BUILD_FCV_IMG_DRAW
#ifdef WITH_FCV_FILL_POLY
#include "modules/img_draw/fill_poly/interface/fill_poly.h"
#endif
#ifdef WITH_FCV_POLY_LINES
#include "modules/img_draw/poly_lines/interface/poly_lines.h"
#endif
#ifdef WITH_FCV_CIRCLE
#include "modules/img_draw/circle/interface/circle.h"
#endif
#ifdef WITH_FCV_LINE
#include "modules/img_draw/line/interface/line.h"
#endif
#endif
