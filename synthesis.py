from image import Image
from labelIntensity import LabelIntensity
from affine import Affine
import numpy as np
import nibabel as nib
import logger
import utils
import sys
import os


class SyntheticModel():

    # Eventually want parameters here
    def __init__(self, args):
        """
        SyntheticModel performs the operations on the image class to create synth images

        Input: arguments
        """
        self.logger_instance = logger.setup_logger()
        self.affine_translation_range = args['affine_translation']
        self.affine_rotation_range = args['affine_rotation']
        self.affine_scaling_range = [
            (100 - args['affine_scaling']) / 100, (100 + args['affine_scaling']) / 100]
        self.downsample_factor = args['downsample_factor']
        self.label_mean = args['mean_label_intensity']
        self.deformation_resolution = args['deformation_resolution']
        self.deformation_sd = args['deformation_sd']
        self.n_images = args['n_images']
        self.inputDir = args['i']
        self.outputDir = args['o']

        self.run()

    def run(self):
        """
        Runs the synthetic model
        """
        self.inputImagePaths = self.cycleData(self.inputDir)
        self.images = [Image(inputImagePath=inputImage, synthModel=self, n_images=self.n_images)
                       for inputImage in self.inputImagePaths]
        self.createTranforms(self.images)
        self.saveImages(self.images, self.outputDir)

    def cycleData(self, inputDir):
        """
        Cycles and loads all data from the base directory
        """
        self.logger_instance.info(
            f"Reading input from {os.path.join(os.getcwd(), inputDir)}")
        niftiFilePaths = []
        for root, dirnames, filenames in os.walk(inputDir):
            for filename in filenames:
                if filename.endswith('.nii.gz'):
                    niftiFilePaths.append(os.path.join(root, filename))

        return niftiFilePaths

    def createTranforms(self, images):
        """
        Creates classes and feed self.images, creating and applying transformations to the Image object dictionaries
        """
        # Affine(images=self.images, translation_range=self.affine_translation_range,
        #       rotation_range = self.affine_rotation_range, scaling_range = self.affine_scaling_range, n_images = self.n_images)

        # Step 1, apply the label intensity
        LabelIntensity(images=self.images)

    def generateDownsampleFactor(self):
        """
        Uniformly samples downsampling factor from a range and adds to the dictionary of transforms
        """
        print('Generating downsampling factors...')
        downsample_list = []
        for i in range(self.n_images):
            downsample_factor = np.random.uniform(
                low=1, high=self.downsample_factor)
            downsample_list.append(downsample_factor)

        return downsample_list

    def saveImages(self, images, outputDir):
        """
        Function to save images to the output directory
        """
        self.logger_instance.info(
            f"Saving images to {os.path.join(os.getcwd(), outputDir)}")
        for image_index, image in enumerate(images):
            base_image_name = os.path.basename(image.inputImagePath)
            for index, matrix in enumerate(image.transformDict['matrices']):
                self.logger_instance.info(
                    f"Saving synth image {index + 1} for image {image_index + 1}")
                output_image_name = base_image_name.replace(
                    '.nii.gz', '_synth_' + str(index) + '.nii.gz')
                output_image_path = os.path.join(
                    outputDir, output_image_name)
                new_image = nib.Nifti1Image(
                    matrix, image.transformDict['affines'][index], image.transformDict['headers'][index])
                nib.save(new_image, output_image_path)
