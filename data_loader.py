import nibabel as nib
import nilearn.plotting as plotting
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


class DataLoader:

    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.images = []
        self.load()
        self.vcheck()

    def load(self):
        """
        Loads the NIFTI data from image path list and saves information in matrix and header attributes

        Takes in: the classes image paths

        Creates: list of dictionaries for each paths image object, image matrix, image header
        """
        for image_path in self.image_paths:
            image = nib.load(image_path)
            imageMatrix = image.get_fdata()
            imageHeader = image.header
            self.images.append({
                'ImageObject': image,
                'ImageMatrix': imageMatrix,
                'ImageHeader': imageHeader
            })

    def vcheck(self):
        """
        Creates a visual check image of the brain and stores it in the inputimages directory
        """
        for image_path in self.image_paths:
            basename = os.path.dirname(image_path)
            plotting.plot_anat(image_path)
            plt.savefig(os.path.join(basename, 'vcheck.png'))
