###
### This homework is modified from CS231.
###


import sys
import numpy as np
import os
from scipy.optimize import least_squares
import math
from copy import deepcopy
from skimage.io import imread
from sfm_utils import *

'''
ESTIMATE_INITIAL_RT from the Essential Matrix, we can compute 4 initial
guesses of the relative RT between the two cameras
Arguments:
    E - the Essential Matrix between the two cameras
Returns:
    RT: A 4x3x4 tensor in which the 3x4 matrix RT[i,:,:] is one of the
        four possible transformations
'''


def estimate_initial_RT(E):
    U, S, Vt = np.linalg.svd(E)

    if np.linalg.det(U) < 0:
        U *= -1
    if np.linalg.det(Vt) < 0:
        Vt *= -1

    R1 = U.dot([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]).dot(Vt)
    R2 = U.dot([[0, -1, 0], [1, 0, 0], [0, 0, 1]]).dot(Vt)

    t = U[:, 2]

    RT1 = np.hstack((R1, t.reshape(3, 1)))
    RT2 = np.hstack((R1, -t.reshape(3, 1)))
    RT3 = np.hstack((R2, t.reshape(3, 1)))
    RT4 = np.hstack((R2, -t.reshape(3, 1)))
    return np.array([RT1, RT2, RT3, RT4])


'''
LINEAR_ESTIMATE_3D_POINT given a corresponding points in different images,
compute the 3D point is the best linear estimate
Arguments:
    image_points - the measured points in each of the M images (Mx2 matrix)
    camera_matrices - the camera projective matrices (Mx3x4 tensor)
Returns:
    point_3d - the 3D point
'''


def linear_estimate_3d_point(image_points, camera_matrices):
    M = len(camera_matrices)

    # Build the matrix A
    A = np.zeros((2 * M, 4))
    for i in range(M):
        A[2 * i, 0] = image_points[i, 0] * camera_matrices[i, 2, 0] - camera_matrices[i, 0, 0]
        A[2 * i, 1] = image_points[i, 0] * camera_matrices[i, 2, 1] - camera_matrices[i, 0, 1]
        A[2 * i, 2] = image_points[i, 0] * camera_matrices[i, 2, 2] - camera_matrices[i, 0, 2]
        A[2 * i, 3] = image_points[i, 0] * camera_matrices[i, 2, 3] - camera_matrices[i, 0, 3]

        A[2 * i + 1, 0] = image_points[i, 1] * camera_matrices[i, 2, 0] - camera_matrices[i, 1, 0]
        A[2 * i + 1, 1] = image_points[i, 1] * camera_matrices[i, 2, 1] - camera_matrices[i, 1, 1]
        A[2 * i + 1, 2] = image_points[i, 1] * camera_matrices[i, 2, 2] - camera_matrices[i, 1, 2]
        A[2 * i + 1, 3] = image_points[i, 1] * camera_matrices[i, 2, 3] - camera_matrices[i, 1, 3]

    # Perform SVD on matrix A
    U, S, V = np.linalg.svd(A)

    # The 3D point is in the last column of Vt
    point_3d = V[-1, :3] / V[-1, 3]

    return point_3d


'''
REPROJECTION_ERROR given a 3D point and its corresponding points in the image
planes, compute the reprojection error vector and associated Jacobian
Arguments:
    point_3d - the 3D point corresponding to points in the image
    image_points - the measured points in each of the M images (Mx2 matrix)
    camera_matrices - the camera projective matrices (Mx3x4 tensor)
Returns:
    error - the 2M reprojection error vector
'''


def reprojection_error(point_3d, image_points, camera_matrices):
    M = len(camera_matrices)
    error = np.zeros(2 * M)

    for i in range(M):
        P = camera_matrices[i]
        x, y = image_points[i]

        projected_point = P.dot(np.append(point_3d, 1))

        error[2 * i] = projected_point[0] / projected_point[2] - x
        error[2 * i + 1] = projected_point[1] / projected_point[2] - y

    return error


'''
JACOBIAN given a 3D point and its corresponding points in the image
planes, compute the reprojection error vector and associated Jacobian
Arguments:
    point_3d - the 3D point corresponding to points in the image
    camera_matrices - the camera projective matrices (Mx3x4 tensor)
Returns:
    jacobian - the 2Mx3 Jacobian matrix
'''


def jacobian(point_3d, camera_matrices):
    M = len(camera_matrices)
    P1, P2, P3 = point_3d[0], point_3d[1], point_3d[2]
    # Initialize the Jacobian matrix
    jacobian = np.zeros((2 * M, 3))

    for i in range(M):
        P = camera_matrices[i, :, :]
        y1 = P[0, 0] * P1 + P[0, 1] * P2 + P[0, 2] * P3 + P[0, 3]
        y2 = P[1, 0] * P1 + P[1, 1] * P2 + P[1, 2] * P3 + P[1, 3]
        y3 = P[2, 0] * P1 + P[2, 1] * P2 + P[2, 2] * P3 + P[2, 3]
        jacobian[2*i, 0] = (y3 * P[0, 0] - y1 * P[2, 0]) / y3**2
        jacobian[2*i, 1] = (y3 * P[0, 1] - y1 * P[2, 1]) / y3**2
        jacobian[2*i, 2] = (y3 * P[0, 2] - y1 * P[2, 2]) / y3**2
        jacobian[2*i+1, 0] = (y3 * P[1, 0] - y2 * P[2, 0]) / y3**2
        jacobian[2*i+1, 1] = (y3 * P[1, 1] - y2 * P[2, 1]) / y3**2
        jacobian[2*i+1, 2] = (y3 * P[1, 2] - y2 * P[2, 2]) / y3**2

    return jacobian


'''
NONLINEAR_ESTIMATE_3D_POINT given a corresponding points in different images,
compute the 3D point that iteratively updates the points
Arguments:
    image_points - the measured points in each of the M images (Mx2 matrix)
    camera_matrices - the camera projective matrices (Mx3x4 tensor)
Returns:
    point_3d - the 3D point
'''


def nonlinear_estimate_3d_point(image_points, camera_matrices):
    point_3d = linear_estimate_3d_point(image_points, camera_matrices)
    num_iterations = 10
    for _ in range(num_iterations):
        error = reprojection_error(point_3d, image_points, camera_matrices)
        jacobian_matrix = jacobian(point_3d, camera_matrices)

        # Solve the linear system using least squares
        delta = np.linalg.lstsq(jacobian_matrix, -error, rcond=None)[0]

        # Update the 3D point
        point_3d += delta

    return point_3d


'''
ESTIMATE_RT_FROM_E from the Essential Matrix, we can compute  the relative RT 
between the two cameras
Arguments:
    E - the Essential Matrix between the two cameras
    image_points - N measured points in each of the M images (NxMx2 matrix)
    K - the intrinsic camera matrix
Returns:
    RT: The 3x4 matrix which gives the rotation and translation between the 
        two cameras
'''


def estimate_RT_from_E(E, image_points, K):
    initial_RT = estimate_initial_RT(E)
    max_positive_z_count = 0
    correct_RT = None
    for i in range(initial_RT.shape[0]):
        positive_count = 0
        RT_i = initial_RT[i, :, :]
        I = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0]
        ])
        camera_matrices = np.zeros((2, 3, 4))
        camera_matrices[0, :, :] = np.dot(K, I)
        camera_matrices[1, :, :] = np.dot(K, RT_i)
        for j in range(image_points.shape[0]):
            point_3d = nonlinear_estimate_3d_point(image_points[j], camera_matrices)
            temp = np.ones((4, 1))
            temp[0:3, :] = point_3d.reshape((3, 1))
            temp1 = RT_i[:, :3].T
            temp2 = -temp1.dot(RT_i[:, 3:])
            A = np.concatenate((temp1, temp2), axis=1)
            point_3d_prime = A.dot(temp)
            if point_3d[2] > 0 and point_3d_prime[2] > 0:
                positive_count += 1
        if positive_count > max_positive_z_count:
            max_positive_z_count = positive_count
            correct_RT = RT_i

    return correct_RT


if __name__ == '__main__':
    run_pipeline = True

    # Load the data
    image_data_dir = 'data/statue/'
    unit_test_camera_matrix = np.load('data/unit_test_camera_matrix.npy')
    unit_test_image_matches = np.load('data/unit_test_image_matches.npy')
    image_paths = [os.path.join(image_data_dir, 'images', x) for x in
                   sorted(os.listdir('data/statue/images')) if '.jpg' in x]
    focal_length = 719.5459
    matches_subset = np.load(os.path.join(image_data_dir,
                                          'matches_subset.npy'), allow_pickle=True, encoding='latin1')[0, :]
    dense_matches = np.load(os.path.join(image_data_dir, 'dense_matches.npy'),
                            allow_pickle=True, encoding='latin1')
    fundamental_matrices = np.load(os.path.join(image_data_dir,
                                                'fundamental_matrices.npy'), allow_pickle=True, encoding='latin1')[0, :]

    # Part A: Computing the 4 initial R,T transformations from Essential Matrix
    print('-' * 80)
    print("Part A: Check your matrices against the example R,T")
    print('-' * 80)
    K = np.eye(3)
    K[0, 0] = K[1, 1] = focal_length
    E = K.T.dot(fundamental_matrices[0]).dot(K)
    im0 = imread(image_paths[0])
    im_height, im_width, _ = im0.shape
    example_RT = np.array([[0.9736, -0.0988, -0.2056, 0.9994],
                           [0.1019, 0.9948, 0.0045, -0.0089],
                           [0.2041, -0.0254, 0.9786, 0.0331]])
    print("Example RT:\n", example_RT)
    estimated_RT = estimate_initial_RT(E)
    print('')
    print("Estimated RT:\n", estimated_RT)

    # Part B: Determining the best linear estimate of a 3D point
    print('-' * 80)
    print('Part B: Check that the difference from expected point ')
    print('is near zero')
    print('-' * 80)
    camera_matrices = np.zeros((2, 3, 4))
    camera_matrices[0, :, :] = K.dot(np.hstack((np.eye(3), np.zeros((3, 1)))))
    camera_matrices[1, :, :] = K.dot(example_RT)
    unit_test_matches = matches_subset[0][:, 0].reshape(2, 2)
    estimated_3d_point = linear_estimate_3d_point(unit_test_matches.copy(),
                                                  camera_matrices.copy())
    expected_3d_point = np.array([0.6774, -1.1029, 4.6621])
    print("Difference: ", np.fabs(estimated_3d_point - expected_3d_point).sum())

    # Part C: Calculating the reprojection error and its Jacobian
    print('-' * 80)
    print('Part C: Check that the difference from expected error/Jacobian ')
    print('is near zero')
    print('-' * 80)
    estimated_error = reprojection_error(
        expected_3d_point, unit_test_matches, camera_matrices)
    estimated_jacobian = jacobian(expected_3d_point, camera_matrices)
    expected_error = np.array((-0.0095458, -0.5171407, 0.0059307, 0.501631))
    print("Error Difference: ", np.fabs(estimated_error - expected_error).sum())
    expected_jacobian = np.array([[154.33943931, 0., -22.42541691],
                                  [0., 154.33943931, 36.51165089],
                                  [141.87950588, -14.27738422, -56.20341644],
                                  [21.9792766, 149.50628901, 32.23425643]])
    print("Jacobian Difference: ", np.fabs(estimated_jacobian
                                           - expected_jacobian).sum())

    # Part D: Determining the best nonlinear estimate of a 3D point
    print('-' * 80)
    print('Part D: Check that the reprojection error from nonlinear method')
    print('is lower than linear method')
    print('-' * 80)
    estimated_3d_point_linear = linear_estimate_3d_point(
        unit_test_image_matches.copy(), unit_test_camera_matrix.copy())
    estimated_3d_point_nonlinear = nonlinear_estimate_3d_point(
        unit_test_image_matches.copy(), unit_test_camera_matrix.copy())
    error_linear = reprojection_error(
        estimated_3d_point_linear, unit_test_image_matches,
        unit_test_camera_matrix)
    print("Linear method error:", np.linalg.norm(error_linear))
    error_nonlinear = reprojection_error(
        estimated_3d_point_nonlinear, unit_test_image_matches,
        unit_test_camera_matrix)
    print("Nonlinear method error:", np.linalg.norm(error_nonlinear))

    # Part E: Determining the correct R, T from Essential Matrix
    print('-' * 80)
    print("Part E: Check your matrix against the example R,T")
    print('-' * 80)
    estimated_RT = estimate_RT_from_E(E,
                                      np.expand_dims(unit_test_image_matches[:2, :], axis=0), K)
    print("Example RT:\n", example_RT)
    print('')
    print("Estimated RT:\n", estimated_RT)

    # Part F: Run the entire Structure from Motion pipeline
    if not run_pipeline:
        sys.exit()
    print('-' * 80)
    print('Part F: Run the entire SFM pipeline')
    print('-' * 80)
    frames = [0] * (len(image_paths) - 1)
    for i in range(len(image_paths) - 1):
        frames[i] = Frame(matches_subset[i].T, focal_length,
                          fundamental_matrices[i], im_width, im_height)
        bundle_adjustment(frames[i])
    merged_frame = merge_all_frames(frames)

    # Construct the dense matching
    camera_matrices = np.zeros((2, 3, 4))
    dense_structure = np.zeros((0, 3))
    for i in range(len(frames) - 1):
        matches = dense_matches[i]
        camera_matrices[0, :, :] = merged_frame.K.dot(
            merged_frame.motion[i, :, :])
        camera_matrices[1, :, :] = merged_frame.K.dot(
            merged_frame.motion[i + 1, :, :])
        points_3d = np.zeros((matches.shape[1], 3))
        use_point = np.array([True] * matches.shape[1])
        for j in range(matches.shape[1]):
            points_3d[j, :] = nonlinear_estimate_3d_point(
                matches[:, j].reshape((2, 2)), camera_matrices)
        dense_structure = np.vstack((dense_structure, points_3d[use_point, :]))

    np.save('results.npy', dense_structure)
    print('Save results to results.npy!')
