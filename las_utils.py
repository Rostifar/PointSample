import numpy as np
import laspy


# Functions for manipulating .las data.


def laspy_obj_to_points(las_obj, chunk_start=0, chunk_end=-1, norm_range=None):
    """
    Inputs: 
        - a laspy object and extracts its pointcloud data
        - if norm_range = (min, max) is supplied, then the pointcloud
          data will be scaled between the range [min, max].
    
    Outputs: pointcloud data of shape: (num_points, (x, y, z)).
    """    
    chunk_end = data.shape[0] if chunk_end == -1 else chunk_end
    data = get_scaled_points(las_obj, chunk_start, chunk_end)

    if norm_range is None:
        return data

    normalize = lambda arr: np.interp(arr, (arr.min(), arr.max()), norm_range)
    data[:, 0] = normalize(data[:, 0]) 
    data[:, 1] = normalize(data[:, 1])
    data[:, 2] = normalize(data[:, 2])
    return data 

    

def get_scaled_points(las_obj, start, end):
    """
    Inputs: a laspy .las object and loads (end - start - 1) points beginning from start.
    Outputs: an np array of points of size: (end - start - 1, 3)
    """
    x = las_obj.X[start : end]
    y = las_obj.Y[start : end]
    z = las_obj.Z[start : end]

    #Scale and translates raw lidar points based on .las header metadata.
    scaled_x = x * las_obj.header.scale[0] + las_obj.header.offset[0]
    scaled_y = y * las_obj.header.scale[1] + las_obj.header.offset[1]
    scaled_z = z * las_obj.header.scale[2] + las_obj.header.offset[2]

    #Ensure data is not corrupted
    assert scaled_x.shape == scaled_y.shape == scaled_z.shape
    return np.vstack((scaled_x, scaled_y, scaled_z)).transpose() 