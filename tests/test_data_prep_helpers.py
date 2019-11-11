
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

    
    def test_no_colocalization(self):
        """
        tests for no colocalization and for different dimmemensionality.
        """

        # note, filepaths are relative to where you run nose.
        width1, height1 = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"
        width2, height2 = 1000, 1000
        anno_file2 = "./Data/Annotation/annotation_output/L1-D01-s_output.csv"

        # Create three separate pixelmaps to use for colocalization testing       
        pixelmap1 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file1,
            width = width1,
            height = height1,
            dot_radius = 2)
        pixelmap2 = dot_click_annoation_file_to_pixelmap(
            anno_file = anno_file2,
            width = width2,
            height = height2,
            dot_radius = 2)

        print(type(pixelmap1))

        # test colocalization with only one pixelmap
        output = colocaliztion([pixelmap1])
        self.assertEqual(output,"Please provide a list of at least two pixelmaps.")

        # test colocalization with different dimension pixelmaps
        output = colocaliztion([pixelmap1,pixelmap2])
        self.assertEqual(output,"Please provide pixelmaps with the same dimensions")


    
    def test_two_colocalization(self):
        """
        tests for two-pixelmap colocalization.
        """

        # note, filepaths are relative to where you run nose.
        width, height = 1024, 1024
        anno_file1 = "./Data/Annotation/annotation_output/L1-D01-g_output.csv"
        anno_file2 = "./Data/Annotation/annotation_output/L1-D01-s_output.csv"

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

        # test colocalization with only two pixelmaps
        output = colocaliztion([pixelmap1,pixelmap2])
        self.assertEqual(output.shape,(width,height))


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
        output = colocaliztion([pixelmap1,pixelmap2,pixelmap3])
        self.assertEqual(output.shape,(width,height))





