import laspy
import numpy as np
import math
import pcl

from open3d import *
from pyflann import *


def visualize_points(data, start, end):
    """
    Inputs: a numpy array data of size (dim, 3) of 3D points.
    Process: Then, data is visualized using Open3D.
    """
    pcd = PointCloud()
    pcd.points = Vector3dVector(data[start:end])
    draw_geometries([pcd])


def get_k_nearest_neighbors(data, start, end, start_test, end_test, k):
    """
    Inputs: a numpy array of 3D points, starting / ending indices, and 
            starting and ending indices for the test portion of data.
    Process: finds the k-nearest neighbors from data[start : end] relative 
            to data[start_test : end_test]
    Outputs: the k-nearest neighbors from the points in data[start : end].
    """
    flann = FLANN()
    result, dists = flann.nn(data[start_test:end_test], data[start:end], 
        k, algorithm="kmeans", branching=32, iterations=7, checks=16)
    get_points = lambda p: data[p]
    return get_points(result).reshape((end - start) * k, 3)


def voxel_filter(data, x_filter, y_filter, z_filter):
    """
    Inputs: a numpy array of 3D points and x_filter, y_filter, z_filter, 
            which determines the size of the voxel grid filter used to subsample data.
    Outputs: a numpy array of voxel filtered points.
    """
    cloud = pcl.PointCloud()
    cloud.from_array(data.astype(np.float32))

    filt = p.make_voxel_grid_filter()
    filt.set_leaf_size(x_filter, y_filter, z_filter)
    return filt.filter().to_array()
    
        

def segment_lowest_points(data, x_len, y_len):
    """
    Inputs: a numpy array of 3D points normalized between [0, 1],
            and integers x_len, y_len.
    Process: 
            - divides [0, 1] into x_len and y_len partitions.
            - for each point in data, finds the x partition and the
              y partition such that x_part - 1 <= point.x <= x_part
                                    y_part - 1 <= point.y <= y_part.
              Then, checks whether point.z is lower the current point.
              If it is, then point is considered the lowest point in that 
              x-y partition.
    Outputs: a numpy array of the lower x_len * y_len points in data.

    """

    x_iter = 1 / x_len
    y_iter = 1 / y_len
    lowest_points = np.ones(shape=(x_len, y_len, 3))

    for i in range(0, data.shape[0]):
        point = data[i, :]
        x = point[0]
        y = point[1]
        z = point[2]
        
        square_x = int(x // x_iter)
        square_y = int(y // y_iter)

        if square_x == x_len:
            square_x = x_len - 1
        if square_y == y_len:
            square_y = y_len - 1

        if lowest_points[square_x, square_y, 2] > z:
            lowest_points[square_x, square_y, :] = point

    for i in range(0, x_len):
        for j in range(0, y_len):
            if lowest_points[i][j] = [1, 1, 1]:
                x_kernel = [i - 1, i + 1]
                y_kernel = [j - 1, j + 1]
                for l in range(0, 2):
                    if x_kernel[l] == x_len or x_kernel[l] == -1:
                        del x_kernel[l]
                    if y_kernel[l] == x_len or y_kernel[l] == -1:
                        del y_kernel[l]
                sigma = 0
                for m in range(0, len(x_kernel)):
                    for n in range(0, len(y_kernel)):
                        sigma += lowest_points[m][n][2]
                lowest_points[i][j] = 
                [((i + 1) * x_iter) / 2, ((j + 1) * x_iter) / 2, sigma / (len(x_kernel) + len(y_kernel))]
    return lowest_points.reshape((x_len * y_len, 3))

           
            
def box_subsample(data, origin, length, width, height):
    """
    Inputs: a numpy array of 3D points, an origin for the box in 3D space,
            the length, width, and height of each box.
    Process: places a length x width x height rectangular prism at origin 
             and finds every point in data within this prism.
    Outputs: a numpy array of points within the prism. 
    """

    p = []
    for i in range(0, 8):
        p.append(np.empty((3, 1)))

    p[0][0, 0] = origin[0] - (length / 2)
    p[0][1, 0] = origin[1] + (width / 2)
    p[0][2, 0] = origin[2]

    p[1][0, 0] = origin[0] + (length / 2)
    p[1][1, 0] = origin[1] + (width / 2)
    p[1][2, 0] = origin[2]

    p[2][0, 0] = origin[0] + (length / 2)
    p[2][1, 0] = origin[1] - (width / 2)
    p[2][2, 0] = origin[2]
    
    p[3][0, 0] = origin[0] - (length / 2)
    p[3][1, 0] = origin[1] - (width / 2)
    p[3][2, 0] = origin[2]

    p[4][0, 0] = p[0][0, 0] 
    p[4][1, 0] = p[0][1, 0]
    p[4][2, 0] = origin[2] + height

    p[5][0, 0] = p[1][0, 0] 
    p[5][1, 0] = p[1][1, 0]
    p[5][2, 0] = origin[2] + height

    p[6][0, 0] = p[2][0, 0] 
    p[6][1, 0] = p[2][1, 0]
    p[6][2, 0] = origin[2] + height

    p[4][0, 0] = p[3][0, 0] 
    p[4][1, 0] = p[3][1, 0]
    p[4][2, 0] = origin[2] + height

    u = np.transpose(p[1] - p[0])
    v = np.transpose(p[3] - p[0])
    w = np.transpose(p[0] - p[4])

    indices = []
    for j in range(0, data.shape[0]):
        point = data[j]
        add_x = p[0][0, 0] <= point[0] and point[0] <= p[1][0, 0]
        add_y = p[2][1, 0] <= point[1] and point[1] <= p[0][1, 0] 
        add_z = p[3][2, 0] <= point[2] and point[2] <= p[4][2, 0]
        if add_x and add_y and add_z:
            indices.append(j)
    new = np.empty((len(indices), 3))
    for k in range(0, len(indices)):
        new[k] = data[indices[k]]
    return new
