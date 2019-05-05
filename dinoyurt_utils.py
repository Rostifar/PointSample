import numpy as np
from las_utils import get_scaled_points 

# Functions for dinoyurt specific functionality, including .out files.


def pointcloud_to_out_file(data, out_path, batch_size = -1):
    """
    Inputs a collection of 3D points and converts the pointcloud data to 
    a .out file; see wiki for .out specification.
    """
    batch_size = data.shape[0] if batch_size == -1 else batch_size
    with open(out_path, 'a') as fil:
        batches = math.ceil(data.shape[0] / batch_size)
        line_num = 1
        for batch_num in range(0, batches):
            lines = []
            for i in range(line_num - 1, min((batch_num + 1) * batch_size, data.shape[0])):
                l1 = str(line_num) + " "
                l2 = str(data[i][0]) + " "
                l3 = str(data[i][1]) + " "
                l4 = str(data[i][2])
                lines.append(l1 + l2 + l3 + l4 + " " + l2 + l3 + l4 + "\n")
                line_num += 1
            fil.writelines(lines)
            batch_num += 1