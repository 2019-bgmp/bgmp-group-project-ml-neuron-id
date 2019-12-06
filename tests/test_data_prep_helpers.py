
from __future__ import print_function
from __future__ import division

import sys
#sys.path.insert(0, ' ../scripts/')

import numpy as np

#from helpers import *
import tests
from DataPrep.helpers import *
import numpy as np

np.random.seed(23)

class TestHelpers(tests.testDataPrep):
    """
    Tests for the TsEncoder class.
    """

    def test_dot_click_annoation_file_to_pixelmap(self):
        """
        Let's test that the correct dimentions are created for each new layer
        """
        # note, filepaths are relative to where you run nose.
        # TODO prep example in super class, see tsenc
        width, height = 1024, 1024
        anno_file = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"

        # make sure the images are the same size        
        pixelmap = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file,
            width = width,
            height = height,
            dot_radius = 2)
        self.assertEqual(pixelmap.shape,(width,height))

        # assert that the number of 1's is geater than number of clicks
        anno_line_count = len(open(anno_file).readlines(  )) 
        self.assertTrue(np.sum(pixelmap) >= anno_line_count)
    
        # TODO more functions.

    
    def test_symquant_to_pixelmap(self):
        """
        Tests for symquant -> pixelmap
        """
        pass

    
    # def test_no_colocalization(self):
    #     """
    #     tests for no colocalization.
    #     """

    #     # note, filepaths are relative to where you run nose.
    #     width1, height1 = 1024, 1024
    #     anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"

    #     # Create three separate pixelmaps to use for colocalization testing       
    #     pixelmap1 = dot_click_annoation_file_to_pixelmap(
    #         anno_file = anno_file1,
    #         width = width1,
    #         height = height1,
    #         dot_radius = 2)

    #     # test colocalization with only one pixelmap
    #     output = colocalization([pixelmap1])
    #     self.a
    #     self.assertEqual(output,"Please provide a list of at least two pixelmaps.")


    
    def test_two_colocalization(self):
        """
        tests for two-pixelmap colocalization.
        """

        # note, filepaths are relative to where you run nose.
        width, height = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"
        anno_file2 = "./Data/Annotation/annotation_output/L1-D01-s_output.csv"

        # Create two separate pixelmaps to use for colocalization testing       
        pixelmap1 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file1,
            width = width,
            height = height,
            dot_radius = 2)
        pixelmap2 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file2,
            width = width,
            height = height,
            dot_radius = 2)


        # test colocalization with only two pixelmaps
        output = colocalization([pixelmap1,pixelmap2])
        self.assertEqual(output.shape,(width,height))

        # test colocalization with smaller arrays for sanity check
        array1 = np.array(([1,0,0],[0,1,0],[0,0,1]))
        array2 = np.array(([0,0,1],[0,1,0],[1,0,0]))
        output = colocalization([array1, array2])
        self.assertTrue(np.array_equal(output, np.array(([0,0,0],[0,1,0],[0,0,0]))))


    def test_three_colocalization(self):
        """
        tests for three-pixelmap colocalization.
        """

        # note, filepaths are relative to where you run nose.
        width, height = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"
        anno_file2 = "./Data/Annotation/annotation_output/L1-D01-s_output.csv"
        anno_file3 = "./Data/Annotation/annotation_output/L1-D01-z_output.csv"

        # Create three separate pixelmaps to use for colocalization testing       
        pixelmap1 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file1,
            width = width,
            height = height,
            dot_radius = 2)
        pixelmap2 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file2,
            width = width,
            height = height,
            dot_radius = 2)
        pixelmap3 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file3,
            width = width,
            height = height,
            dot_radius = 2)

        # test colocalization with three pixelmaps
        output = colocalization([pixelmap1,pixelmap2,pixelmap3])
        self.assertEqual(output.shape,(width,height))



    def test_empirical_subpatch(self):
        """
        tests for sub-patching empirical images
        """

        empiricalg = "./Data/Empirical/L1-D01-g.bmp"
        empiricals = "./Data/Empirical/L1-D01-s.bmp"
        empiricalz = "./Data/Empirical/L1-D01-z.bmp"
        
        output = empirical_prep([empiricalg])
        self.assertEqual(output.shape, (384,32,32,1))

        output = empirical_prep([empiricalg, empiricals])
        self.assertEqual(output.shape, (384,32,32,2))

        output = empirical_prep([empiricalg, empiricals, empiricalz])
        self.assertEqual(output.shape, (384,32,32,3))

        output = empirical_prep([empiricalg, empiricals], size=64)
        self.assertEqual(output.shape, (96,64,64,2))



    def test_pixelmap_subpatch(self):
        """
        tests for sub-patching empirical images
        """

        # note, filepaths are relative to where you run nose.
        width1, height1 = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"

        # Create one pixelmap for sub-patch testing       
        pixelmap1 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file1,
            width = width1,
            height = height1,
            dot_radius = 2)

        sub_annotations = sub_patch_pixelmap(pixelmap1)
        self.assertEqual(sub_annotations.shape,(384,32,32))

        sub_annotations = sub_patch_pixelmap(pixelmap1, size=64)
        self.assertEqual(sub_annotations.shape,(96,64,64))




    def test_synquant_colocalization(self):
        anno_file1='./Data/Annotation/synquant_output/z=4/RoiSet_g.zip'
        anno_file2='./Data/Annotation/synquant_output/z=4/RoiSet_s.zip'
        anno_file3='./Data/Annotation/synquant_output/z=4/RoiSet_z.zip'
        pixelmap1=synquant_to_pixelmap(anno_file1)
        pixelmap2=synquant_to_pixelmap(anno_file2)
        pixelmap3=synquant_to_pixelmap(anno_file3)
        synquant_colocalization_map = colocalization([pixelmap1,pixelmap2,pixelmap3])

        # img = plt.imshow(synquant_colocalization_map)
        # plt.show(img)
        self.assertEqual(synquant_colocalization_map.shape,(1024,1024))


    def test_f1_score(self):
        """
            tests for calculating f1 score
        """

        syn_file1='./Data/Annotation/synquant_output/z=4/RoiSet_g.zip'
        syn_file2='./Data/Annotation/synquant_output/z=4/RoiSet_s.zip'
        syn_file3='./Data/Annotation/synquant_output/z=4/RoiSet_z.zip'
        pixelmap11=synquant_to_pixelmap(syn_file1)
        pixelmap22=synquant_to_pixelmap(syn_file2)
        pixelmap33=synquant_to_pixelmap(syn_file3)
        synquant_colocalization_map = colocalization([pixelmap11,pixelmap22,pixelmap33])

        width, height = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"
        anno_file2 = "./Data/Annotation/annotation_output/L1-D01-s_output.csv"
        anno_file3 = "./Data/Annotation/annotation_output/L1-D01-z_output.csv"

        # Create three separate pixelmaps to use for colocalization testing       
        pixelmap1 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file1,
            width = width,
            height = height,
            dot_radius = 2)
        pixelmap2 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file2,
            width = width,
            height = height,
            dot_radius = 2)
        pixelmap3 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file3,
            width = width,
            height = height,
            dot_radius = 2)

        # test colocalization with three pixelmaps
        phil_output = colocalization([pixelmap1,pixelmap2,pixelmap3])

        # print(synquant_colocalization_map.shape)
        # print(phil_output.shape)
        # self.assertEqual(synquant_colocalization_map.shape,(1024,1024))
        # self.assertEqual(phil_output.shape,(1024,1024))
        f1_output = f1_score(synquant_colocalization_map, phil_output)
        self.assertTrue(f1_output >= 0)
        self.assertTrue(f1_output <= 1)


        # simple f1 test to double check
        array1 = np.array(([1,0,0],[0,1,0],[0,0,1]))
        array2 = np.array(([0,0,1],[0,1,0],[1,0,0]))
        F1_test = f1_score(array1, array2)
        self.assertEqual(F1_test, (1/3))



    def test_generate_simulated_microscopy_sample(self):
        """
            tests for simulating one target and one set of three example images
        """

        width = 32
        height = 32

        x,y = generate_simulated_microscopy_sample(colocalization = [1,1,1,1,1,1,1], 
        width=width, height=height, coloc_thresh = 2)

        # Test x and y shape
        self.assertEqual(x.shape, (32,32,3))
        self.assertEqual(y.shape, (32,32))

        # Test to make sure x and y have the same number of 0s within
        example_zero_count_channel0 = 0
        example_zero_count_channel1 = 0
        target_zero_count = 0
        for i in range(height):
            for j in range(width):
                if(x[i][j][0] == 0):
                    example_zero_count_channel0 += 1
                if(x[i][j][1] == 0):
                    example_zero_count_channel1 += 1
                if(y[i][j] == 0):
                    target_zero_count += 1
        self.assertEqual(example_zero_count_channel0, target_zero_count)
        self.assertEqual(example_zero_count_channel1, target_zero_count)


        x,y = generate_simulated_microscopy_sample(colocalization = [0,0,0,1,0,0,0], 
        width=32, height=32, coloc_thresh = 2)

        # Test x and y shape
        self.assertEqual(x.shape, (32,32,3))
        self.assertEqual(y.shape, (32,32))

        # Test to make colocalization is working properly
        example_zero_count_channel0 = 0
        example_zero_count_channel1 = 0
        target_zero_count = 0
        for i in range(height):
            for j in range(width):
                if(x[i][j][0] == 0):
                    example_zero_count_channel0 += 1
                if(x[i][j][1] == 0):
                    example_zero_count_channel1 += 1
                if(y[i][j] == 0):
                    target_zero_count += 1
        self.assertEqual(example_zero_count_channel0, target_zero_count)
        # channel one should have more 0s than the target because on this test there is only colocalization between channel 0 and 2
        self.assertTrue(example_zero_count_channel1 > target_zero_count)


        x,y = generate_simulated_microscopy_sample(colocalization = [0,0,0,1,0,0,0], 
        width=32, height=32, coloc_thresh = 3)

        # Test x and y shape
        self.assertEqual(x.shape, (32,32,3))
        self.assertEqual(y.shape, (32,32))

        # Test to make sure coloc_thresh is working properly
        example_zero_count_channel0 = 0
        example_zero_count_channel2 = 0
        target_zero_count = 0
        for i in range(height):
            for j in range(width):
                if(x[i][j][0] == 0):
                    example_zero_count_channel0 += 1
                if(x[i][j][2] == 0):
                    example_zero_count_channel2 += 1
                if(y[i][j] == 0):
                    target_zero_count += 1
        self.assertEqual(example_zero_count_channel2, example_zero_count_channel0)
        # channel one and the target should have the same number of 0s because the coloc_thresh was set to 3
        self.assertEqual(example_zero_count_channel1, target_zero_count)
        self.assertTrue(target_zero_count > example_zero_count_channel0)
        
        
            
    def test_generate_whole_dataset_stub(self):
        """
            tests for simulating one target and one set of three example images
        """
        
        x,y = generate_whole_dataset(2000)

        self.assertEqual(x.shape, (2000, 32, 32, 3))
        self.assertEqual(y.shape, (2000, 32, 32, 1))
