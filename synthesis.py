import numpy as np
import utils


class SyntheticModel():

    # Eventually want parameters here
    def __init__(self, args):
        """
        SyntheticModel performs the operations on the image class to create synth images

        Input: arguments
        """
        self.args = args

    def affineTransform(self, matrix, header, n_images):
        """
        For all NIFTI data, create new attribute with dictionary 
        """
        for i in range(n_images):
            affine_translation_scaling = 1 / header['pixdim'][1]

        return
