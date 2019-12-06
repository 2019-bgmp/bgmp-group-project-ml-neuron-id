from helpers import *
import numpy as np
#priInt(ll)

# for i in range(5):
#     x,y = generate_simulated_microscopy_sample(colocalization = [1,1,1,1,1,1,1], 
#         width=32, height=32, coloc_thresh = 2)
#     # x,y = generate_simulated_microscopy_sample(colocalization = [0,0,0,1,0,0,0], 
#     #     width=32, height=32, coloc_thresh = 2)
#     # x = np.zeros([32,32,3])
    
#     add_normal_noise_to_image(x,1.0)
#     plt.imshow(x)
#     plt.show()
#     plt.imshow(y)
#     plt.show()



# Simulate datasets

### BACKGROUND
### Dataset of size 10000 with only background noise
# x,y = generate_whole_dataset_stub(10000,percent_zero = 1,
#                                         percent_one = 0,
#                                         percent_two = 0,
#                                         percent_three = 0,
#                                         percent_four = 0,
#                                         percent_five = 0)
# add_normal_noise_to_image(x,1.0)
# x.dump('../Data/Simulated/Background_sample_simulated')
# y.dump('../Data/Simulated/Background_target_simulated')

### EASY
### Dataset of 10000 with only complete colocalization and some background
# # colocal_list = [[[0,0,0,0,0,0,0]],
# #                     [[1,0,0,0,0,0,0]],#, [0,1,0,0,0,0,0], [0,0,1,0,0,0,0]],
# #                     [[2,0,0,0,0,0,0]],#, [0,2,0,0,0,0,0], [0,0,2,0,0,0,0], [0,1,1,0,0,0,0], [1,0,1,0,0,0,0]],
# #                     [[3,0,0,0,0,0,0]],#, [0,3,0,0,0,0,0], [0,0,3,0,0,0,0], [1,1,1,0,0,0,0], [2,0,1,0,0,0,0]],
# #                     [[4,0,0,0,0,0,0]],#, [0,4,0,0,0,0,0], [0,0,4,0,0,0,0], [2,1,1,0,0,0,0], [1,2,1,0,0,0,0]],
# #                     [[5,0,0,0,0,0,0]],#, [0,5,0,0,0,0,0], [0,0,5,0,0,0,0], [2,1,2,0,0,0,0], [2,2,1,0,0,0,0]],
# #                     ]
# x,y = generate_whole_dataset_stub(10000,percent_zero = 0.25,
#                                         percent_one = 0.2,
#                                         percent_two = 0.2,
#                                         percent_three = 0.2,
#                                         percent_four = 0.1,
#                                         percent_five = 0.05,
#                                         coloc_thresh=3)
# add_normal_noise_to_image(x,0.1)
# x.dump('../Data/Simulated/Easy_sample_simulated')
# y.dump('../Data/Simulated/Easy_target_simulated')


### COLOCALIZATION
### Dataset of 10000 images with various amounts of colocalization and some background
### A background noise of 0.3 was added to the x images in this dataset
x,y = generate_whole_dataset_stub(10000,percent_zero = 0.25,
                                        percent_one = 0.2,
                                        percent_two = 0.2,
                                        percent_three = 0.2,
                                        percent_four = 0.1,
                                        percent_five = 0.05,
                                        coloc_thresh=3)
add_normal_noise_to_image(x,0.3)
x.dump('../Data/Simulated/Colocalization_sample_simulated')
y.dump('../Data/Simulated/Colocalization_target_simulated')
