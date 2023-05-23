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
        self.new_images = []

        self.load()
        for image_path in self.image_paths:
            self.vcheck(image_path)

    def vcheck(self, image_path, number=None):
        """
        Creates a visual check image of the brain and stores it in the inputimages directory
        """
        basename = os.path.dirname(image_path)
        plotting.plot_anat(image_path)
        if number == None:
            plt.savefig(os.path.join(basename, 'vcheck.png'))
        elif number != None:
            plt.savefig(os.path.join(
                basename, 'vcheck_' + str(number) + '.png'))

    def transformDictionary(self):
        """
        Declares the transform dictionary which contains lists for each transform of the image

        Output: dict
        """
        transforms = {
            'matrices': [],
            'headers': [],
            'affineTranslation': [],
            'affineRotation': [],
            'affineScaling': [],
            'affineTransform': [],
            'downsampleFactor': [],
            'labelIntensityMean': []
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
            imageAffine = image.affine
            self.images.append(
                Image(imageMatrix, imageHeader, imageAffine, self.transformDictionary(), self.synthModel))

    def write(self, new_matrix, header, input_data_path, count, affine):
        """
        Writes all the new images to the OutputImages folder under a subject directory

        Input: self.new_images (list of lists, first layer is an element for each input image, second layer is n length for new images based on each image)

        Output: output nifti files in Data/OutputImages
        """
        print('Writing to output...')
        # Create a new NiftiImage
        image = nib.Nifti1Image(new_matrix, affine, header)

        # Save the affine to output destination
        subject_input_folder = os.path.dirname(input_data_path)
        subject_name = os.path.basename(subject_input_folder)
        input_folder = os.path.dirname(subject_input_folder)
        data_folder = os.path.dirname(input_folder)
        output_folder = os.path.join(data_folder, 'OutputImages', subject_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_path = os.path.join(
            output_folder, subject_name + '_' + str(count) + '_Synth_T1w.nii.gz')
        nib.save(image, output_path)
        self.vcheck(output_path, count)

    def makeTransforms(self, n_images):
        """
        Generate n_images synthetic transforms
        """
        for image in self.images:
            image.synthTransforms(n_images)

    def applyTransforms(self):
        """
        Apply synthetic transforms to images
        """
        for base_index, image in enumerate(self.images):
            new_image_matrices, new_image_headers = image.synthImages()
            for new_image_index, new_image in enumerate(new_image_matrices):
                self.write(new_image, new_image_headers[new_image_index],
                           self.image_paths[base_index], new_image_index, image.affine)
