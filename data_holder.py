from image import Image
import nibabel as nib
import nilearn.plotting as plotting
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


class DataHolder:

    def __init__(self, image_paths, synthModel):
        self.image_paths = image_paths
        self.synthModel = synthModel
        self.images = []

        self.load()
        self.vcheck()

    def transformDictionary(self):
        transforms = {
            'affineTransform': []
        }

        return transforms

    def load(self):
        """
        Loads the NIFTI data from image path list and saves information in matrix and header attributes

        Takes in: the classes image paths

        Creates: list of dictionaries for each paths image object, image matrix, image header, initalizes transform dictionary
        """
        for image_path in self.image_paths:
            image = nib.load(image_path)
            imageMatrix = image.get_fdata()
            imageHeader = image.header
            self.images.append(
                Image(imageMatrix, imageHeader, self.transformDictionary(), self.synthModel))

    def vcheck(self):
        """
        Creates a visual check image of the brain and stores it in the inputimages directory
        """
        for image_path in self.image_paths:
            basename = os.path.dirname(image_path)
            plotting.plot_anat(image_path)
            plt.savefig(os.path.join(basename, 'vcheck.png'))

    def runSynth(self, n_images):
        for image in self.images:
            image.synthImages(n_images)
