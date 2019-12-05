from helpers import *
#priInt(ll)

for i in range(5):
    x,y = generate_simulated_microscopy_sample(colocalization = [3,0,0,0,0,0,0], 
        width=100, height=100, min_radius = 1, max_radius=7,coloc_thresh = 3)
    # x,y = generate_simulated_microscopy_sample(colocalization = [0,0,0,1,0,0,0], 
    #     width=32, height=32, coloc_thresh = 2)
    # x = np.zeros([32,32,3])
    
    add_normal_noise_to_image(x,1.0)
    plt.imshow(x)
    plt.show()
    plt.imshow(y)
    plt.show()
