
"""
File: Helpers.py
Authors Jared Galloway, Nick Wagner, Annie Wang
Date: 11/20/2019

This file contains all helpful python
functions for scripts included in synapse detection.
"""

##############################################################################

import os
import sys

import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.draw import circle
#import cv2
from mpl_toolkits.mplot3d import Axes3D
#from read_roi import read_roi_zip

##############################################################################

# UNDER CONSTRUCTION
def dot_click_annoation_file_to_pixelmap(anno_file,
                                                width,
                                                height,
                                                dot_radius):
    """
    This function takes in an csv image anno which has the
    row format: filepath, top x, top y, bottom x, bottom y. no header.
    
    

    width, and height represent the total size of the annotated image.
    dot_radius is the size the of the circle centered around a clicked 
    synapse. 
 
    EX INPUT

    L1-D01-g.bmp,583,247,591,255,synapse
    L1-D01-g.bmp,589,256,597,264,synapse
    L1-D01-g.bmp,559,269,567,277,synapse
    L1-D01-g.bmp,592,267,600,275,synapse
    L1-D01-g.bmp,635,264,643,272,synapse
    L1-D01-g.bmp,607,281,615,289,synapse
    L1-D01-g.bmp,595,284,603,292,synapse

    the function will return a 2-dimentional binary numpy ndarray object 
    with the shape (width,height). 1's represent annotated images 
    
    """

    # initialize a pixelmap
    pixelmap = np.zeros([width,height], dtype=np.uint8)

    # draw ones using skimage circle()
    # https://scikit-image.org/docs/dev/api/skimage.draw.html
    # skimage.draw.circle
    for line in open(anno_file,"r"):

        # [filepath, top x, top y, bottom x, bottom y]
        anno = line.strip().split(',')
       
        # these should be the original x, and y's when given a bbox. 
        mid_x = (int(anno[1]) + int(anno[3])) // 2
        mid_y = (int(anno[2]) + int(anno[4])) // 2

        assert(0 <= mid_x <= width)  # annotation out of range
        assert(0 <= mid_y <= height) # annotation out of range

        # yay skimage!
        rr,cc = circle(mid_x, mid_y, dot_radius)

        # cut out extreneous indices.
        count = 0
        for i in range(len(rr)):
            if (rr[i-count] >= 1024 or rr[i-count] < 0):
                rr = np.delete(rr, i-count)
                cc = np.delete(cc, i-count)
                count += 1
            if (cc[i-count] >= 1024 or cc[i-count] < 0):
                rr = np.delete(rr, i-count)
                cc = np.delete(cc, i-count)
                count += 1
         
        # set pixel values.
        pixelmap[rr, cc] = 1

    return pixelmap

##############################################################################

def synquant_to_pixelmap(filename):
    """
    TODO: comment
    
    This function should take in the output from SynQuant
    https://www.biorxiv.org/content/10.1101/538769v1
    and convert it to a pixelmap 

        
    """

    
    roi = read_roi_zip(filename)
    xcoord=[]
    ycoord=[]
    for i in roi.keys():
        xcoord=np.append(xcoord,(roi[i]['x']))
        ycoord=np.append(ycoord,roi[i]['y'])
    xcoord=xcoord.astype(int)
    ycoord=ycoord.astype(int)
    map = np.zeros((1024,1024),dtype=int)
    for i in range(len(xcoord)):
        map[xcoord[i]-1,ycoord[i]-1]+=1

    return map

##############################################################################

def colocalization(pixelmap_list):
    """
    This function takes in a list of pixelmaps and performs bitwise operations 
    to find the spots that have pixels in common (colocalization)


    This function is dependent on the length of the pixelmap_list. If the length is
    just two then it will compute the bitwise-AND, and find the spots of colocalization
    for those two images. If the length is three then it will find all three sets of 
    image colocalization and bitwise-OR those together.


    This function will return a 2-dimentional binary numpy ndarray object 
    with the shape (1024,1024). 1's represent any point of colocalization between the
    images.
    """
    pixelmap_list = np.array(pixelmap_list)

    SHAPE = pixelmap_list[0].shape
    COLOCALIZED = np.zeros((SHAPE[0],SHAPE[1]), dtype=np.uint8)

    # if(len(pixelmap_list) == 1):   # The user did not provide enough information to calculate the colocalization
    #     return "Please provide a list of at least two pixelmaps."
    assert(len(pixelmap_list) >= 2)
    
    
    # Case where two pixelmaps are provided
    if(len(pixelmap_list) == 2):
        if(pixelmap_list[0].shape != pixelmap_list[1].shape):
            return "Please provide pixelmaps with the same dimensions"
        
        # performs a bitwise-AND to keep only the pixels that share a spot of colocalizaiton
        COLOCALIZED = np.bitwise_and(pixelmap_list[0], pixelmap_list[1])
    

    # Case where three pixelmaps are provided
    if(len(pixelmap_list) == 3):
        if(pixelmap_list[0].shape != pixelmap_list[1].shape or pixelmap_list[0].shape != pixelmap_list[2].shape):
            return "Please provide pixelmaps with the same dimensions"

        # performs three bitwise-ANDs to keep only the pixels that share a spot of colocalizaiton
        coloalized1 = np.bitwise_and(pixelmap_list[0], pixelmap_list[1])
        coloalized2 = np.bitwise_and(pixelmap_list[0], pixelmap_list[2])
        coloalized3 = np.bitwise_and(pixelmap_list[1], pixelmap_list[2])

        # performs two bitwise-ORs to combine all three sets of colocalization
        COLOCALIZED = np.bitwise_or(coloalized1, coloalized2)
        COLOCALIZED = np.bitwise_or(COLOCALIZED, coloalized3)

    
    return COLOCALIZED

##############################################################################

def sub_patch_pixelmap(image_pixelmap, size=32, height=(256,1024), width=(256,768)):
    """
    This function allows the user to break up the given pixelmap into sub-patches. The 
    user can specify the area they would like to sub-patch as well as the size of
    the patch they would like to grab.

    image_pixelmap: numpy 2d array corresponding to the pixelmap to be sub-patched
    size: the SIZExSIZE chunk to be grabbed
    height: tuple specifying the y start and stop positions (start, stop)  
            DEFAULT: (256,1024)
    width: tuple specifying the x start and stop positions (start, stop)  
            DEFAULT: (256,768)
    
    This function will return a numpy ndarray of SIZExSIZE 2-dimentional binary numpy ndarrays
    """

    SUB_IMAGES = []    # initialize an array for holding the sub images

    for i in range(height[0],height[1],size):  # this for loop isolates only the region of the image specified in the parameters
        for j in range(width[0],width[1],size):
            temp_array = image_pixelmap[i:i+size,j:j+size] # grabbing SIZExSIZE chunks and storing them in an array
            SUB_IMAGES.append(temp_array)
    
    SUB_IMAGES = np.array(SUB_IMAGES)

    return SUB_IMAGES

##############################################################################

def empirical_prep(list_of_paths, size=32, height=(256,1024), width=(256,768)):
    """
    This function allows the user to break up the empirical images into sub images for 
    training or testing. The user can give as many paths to images as they would like in
    the list_of_paths parameter. The user can specify the area they would like to sub-image 
    as well as the size of the chunk they would like to grab.

    list_of_paths: list of strings corresponding to the paths of the images wanting to be
                sub-imaged
    size: the SIZExSIZE chunk to be grabbed
    height: tuple specifying the y start and stop positions (start, stop)  
            DEFAULT: (256,1024)
    width: tuple specifying the x start and stop positions (start, stop)  
            DEFAULT: (256,768)

    This function will return a list of numpy ndarrays, of which contain all of the sub-images
    for that given empirical image. There will be one item in the list for each empirical 
    image given
    """

    sub_empirical = []
    for num in range(len(list_of_paths)):
        pillow_opened_image = Image.open(list_of_paths[num])
        temp_sub_images = []
        for i in range(height[0],height[1],size):  # this for loop isolates only the region of the image specified in the parameters
            for j in range(width[0],width[1],size):
                temp_pic = pillow_opened_image.crop((i,j,i+size,j+size)) # grabbing SIZExSIZE chunks and storing them in an array
                # 7
                temp_pic = np.array(temp_pic)[:,:,0]
                temp_sub_images.append(temp_pic)
        temp_sub_images = np.array(temp_sub_images)
        sub_empirical.append(temp_sub_images)
    
    sub_empirical = np.array(sub_empirical)
    
    # here, we are re-arranging the axes so 
    # we have (batch, height, width, channels)
    sub_empirical = np.swapaxes(sub_empirical,0,1)
    sub_empirical = np.swapaxes(sub_empirical,1,2)
    sub_empirical = np.swapaxes(sub_empirical,2,3)
    

    return sub_empirical

##############################################################################

def f1_score(pixelmap1, pixelmap2):
    """
    this function will take two pixelmaps (2d-ndarray)
    and return the f1 score defined as:
    
    f1 = 2 / ((1 / precision) + (1/ recall)).
    precision = true positive / (true positive + false positiv)
    recall = true positive / (true positive + false negative)


    pixelmap1, pixelmap2: two pixelmaps of the same size which we would like
    to evaluate and get a metric of how they compare

    This function will return a float value between 0 and 1. 0 being the worst
    the model could be doing amd 1 being the best.
    """
    assert(pixelmap1.shape == pixelmap2.shape)

    true_positive = np.sum(np.bitwise_and(pixelmap1, pixelmap2))
    false_positive = np.sum(np.bitwise_and(pixelmap1, ~pixelmap2))
    false_negative = np.sum(np.bitwise_and(~pixelmap1, pixelmap2))

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)

    return 2/((1/precision) + (1/recall))

##############################################################################

# TODO Impliment
def generate_whole_dataset_stub():
    """
    Come up with a simpler interface for running and saving a bunch of 
    these images.
    """
    pass

##############################################################################

# TODO This could obviously be made much more complex
def add_normal_noise_to_image(image, gaussian_bg_sd, background_only = True):
    """
    this image adds background noise (absolute value 
    Gaussian centered at zero) with variance gaussian_bg_sd,
    to each pixel channel which is currently
    not already activated (activation 0). 

    for more noise, simply add variance.
    """
    # add background noise to an image
    gaussian_bg_mean = 0
    bg = np.abs(np.random.normal(gaussian_bg_mean, gaussian_bg_sd, image.shape))

    # add the noise to image param, skipping the dots, if required
    # image[image == 0] += bg[image == 0] if backgound_only else image += bg
    if background_only:
        image[image == 0] += bg[image == 0] 
    else:
        image += bg

    # correct for values above 1!
    image[image > 1] = 1

    

##############################################################################

def generate_simulated_microscopy_sample(
        colocalization = [5] + [0 for _ in range(6)],
        width = 32,
        height = 32,
        radius = 2,
        coloc_thresh = 3
        ):
    
    # TODO max radius size? make a radius vector for each layer of
    # x,y coordinates to introduce some more noise! mo betta.

    # TODO Clean up and re-do docs and testing!



    """
    :param: colocalization <list> - a list which contains the 7 colocal counts!
        the params should be in the following order:
            idx - colocal meaning
            0 - all_layers share. as well as the pixelmap
            1 - just the 0, and 1 share
            2 - just the 1 and 2 share
            3 - just the 0 and 2 share
            4 - just 0
            5 - just 1
            6 - just 2
            
    :param: width <int> - width of the sample 
    
    :param: height <int> - height of the sample
    
    :param: radius <int> - radius of bumps

    :return: (3D numpy tensor, 2D numpy tensor) - this is going to 
        be the simulated 

    Here, we take in amount of spots wanted as either colocalized
    on any combination of channels 0, 1, and 2, or singlet on any layer.

    This leaves 7 possibilities:
        
        1X Complete Co-localization - all layers have this bump
        3X double co-loc, 3 choose 2 combinations of co-pair-bumps
        3X singlet bumps


    Given these 7 params, this function computes the x,y vectors
    for each three layers so they may be created seperately and 
    finally stacked into the 3D tensor representing simulated 
    confocal image with parameterized co-localization. 
    """
    
    assert(len(colocalization) == 7)
    assert(radius < (width // 2) and radius < (height // 2))
    assert(coloc_thresh in [1,2,3])
    
    # initialize out empty layers.
    #layer0, layer1, layer2, pixelmap = ([] for _ in range(4))

    # Hm, if you bored, you could generalize this 
    # colocalization algorithm getting all combinations in a set
    
    # the first three are the layers for the simulated sample,
    # the last later is the pixelmap target
    layers_list = [[] for _ in range(4)]
    combs = [[0,1,2],[0,1],[1,2],[0,2],[0],[1],[2]]
  
    for i,layers in enumerate(combs):
        for num_dots in range(colocalization[i]):
            x = np.random.randint(radius, width - radius)
            y = np.random.randint(radius, height - radius)
            for layer_index in layers:
                layers_list[layer_index] += [(x,y)]
            if len(layers) >= coloc_thresh:
                layers_list[3] += [(x,y)]

    channels = [simulate_single_layer(
        layers_list[i], width, height, radius) for i in range(3)]
    simulated_sample = np.stack(channels,axis=2)    
    pixelmap_target = simulate_single_layer(
        layers_list[3], width, height, radius, is_pixelmap = True)

    return simulated_sample, pixelmap_target

##############################################################################

def simulate_single_layer(
        xy_list,
        width,
        height,
        radius,
        is_pixelmap = False,
        ):
    """
    This function will simulate a single layer given the coordinates for each 
    exponential bump!
    """    
    

    # not implimented yet
    assert(type(radius) == int)

    # init the tensor to be returned.
    sim_bump = np.zeros([width, height])

    # Step through all the x,y locations where the dots will be located 
    # on each channel,
    for x,y in xy_list:
    
        # Draw nice circle and init an array to store
        # respective activations,
        xx,yy = circle(x,y,radius)
        if is_pixelmap:
            sim_bump[xx,yy] = 1
            continue

        activation_list = np.zeros(len(xx))

        # for each location that is a synapse
        # we are going to compute the activation 
        for i in range(len(xx)):

            # use pythagorian theorem to compute radius on discrete space!
            diff_from_center = math.sqrt((xx[i] - x)**2 + (yy[i] - y)**2)

            # This is where we sample from the exponential "bump"
            # Question, How dow we make this bump wider, @ Annie
            # I would like for the majority of the numbers not to 
            # be so small :)
            activation = np.exp(-(diff_from_center**2))
       
            # we then add guassian noise the add another level of randomness 
            activation_list[i] = activation + np.abs(np.random.normal(0,0.1))

        # finally, population the tensor.
        sim_bump[xx,yy] += activation_list

    # Okay here, lets correct for the number things greater and equal to one.
    # the main idea is: a by-product of our algorithm is that the center of all
    # synapses have an activation == to 1. we should correct for this 
    # because it's not realistic
    # TODO This could be done slightly more effeciently.
    if not is_pixelmap:
        sim_bump[sim_bump > 1] = 1
        num_ones = len(sim_bump[sim_bump == 1])
        sim_bump[sim_bump == 1] += -1 * np.abs(np.random.normal(0,0.1,num_ones))
    
    assert(len(sim_bump[sim_bump > 1]) == 0)

    return sim_bump


##############################################################################

def tensor_to_3dmap(tensor, out = None):
    """
    A function which takes in a 2D numpy array and produces 
    a heatmap.

    if a filename is given to out then it will save the fig,
    otherwise it will attempt to open the png with matplotlib.
    """

    X = np.arange(0, tensor.shape[0])
    Y = np.arange(0, tensor.shape[1])
    X, Y = np.meshgrid(X, Y)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, tensor, rstride=1, 
        cstride=1, cmap='hot', linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    if out == None:
        plt.show()
    else:
        plt.savefig(out)

    return None

##############################################################################

def simple_simulator(num_samples, width, height, 
        coloc_thresh, colocalization, noise):
    """
    A very non-complex simulator
    """

    x = np.zeros([num_samples, width, height, 3])
    y = np.zeros([num_samples, width, height])
    for i in range(num_samples):
        X, Y = generate_simulated_microscopy_sample(
            colocalization = colocalization,
            width = width,
            height = height,
            coloc_thresh = 3)

        add_normal_noise_to_image(X,0.2)
        x[i] = X
        y[i] = Y

    y = np.reshape(y, [num_samples, width, height, 1])
    
    return x, y

