# This file creates a class called 'image' that contains data about a loaded NIFTI image
# Will also import functions from synthesis that creates synthetic images and adds to this class

from synthesis import SyntheticModel
import numpy as np


class Image:

    def __init__(self, imageMatrix, imageHeader, transformDictionary, synthModel):
        self.matrix = imageMatrix
        self.header = imageHeader
        self.transformDictionary = transformDictionary
        self.synthModel = synthModel

    def synthImages(self, n_images):
        affines = self.synthModel.affineTransform(
            self.matrix, self.header, n_images)
