from subsample import get_k_nearest_neighbors
from subsample import visualize_points
from las_utils import laspy_obj_to_points


#### MODIFY BEFORE RUNNING ####
las_file = ""
####

print ("Running voxel_filter subsampling with " + las_file)
lidar = laspy.file.File(las_file)

# Get total number of points
model_size = lidar.X.shape[0]

# Convert .las file to points
data = laspy_obj_to_points(lidar, chunk_start=0, chunk_end=model_size, norm_range=(0, 1))

# Segment using segment_lowest_points
new_data = get_k_nearest_neighbors(data, 0, model_size, 0, model_size)

visualize_points(new_data[:, [0, 2, 1]], 0, new_data.shape[0])