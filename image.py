# This file creates a class called 'image' that contains data about a loaded NIFTI image
# Will also import functions from synthesis that creates synthetic images and adds to this class

from synthesis import SyntheticModel
import numpy as np


class Image:

    def __init__(self, imageMatrix, imageHeader, affine, transformDictionary, synthModel):
        self.matrix = [imageMatrix]
        self.header = imageHeader
        self.affine = affine
        self.transformDictionary = transformDictionary
        self.synthModel = synthModel

    def synthTransforms(self, n_images):
        print('Generating affine transforms...' + '\n')

        # Make copies of matrix
        self.transformDictionary['matrices'] = self.synthModel.copyMatrices(
            self.matrix, n_images)

        # Make copies of headers
        self.transformDictionary['headers'] = self.synthModel.copyHeaders(
            self.header, n_images)

        # If parameter is not 0, generate affine translations
        if self.synthModel.affine_translation_range != 0:
            self.transformDictionary['affineTranslation'] = self.synthModel.generateAffineTranslation(
                self.header, n_images)
        # If it is 0, fill the translation lookup with 0
        else:
            self.transformDictionary['affineTranslation'] = [
                np.zeros((3,), dtype=int) for i in range(n_images)]

        # Rotation
        if self.synthModel.affine_rotation_range != 0:
            self.transformDictionary['affineRotation'] = self.synthModel.generateAffineRotation(
                n_images)
        else:
            self.transformDictionary['affineRotation'] = [
                [np.array[1, 0, 0], np.array[0, 1, 0], np.array[0, 0, 1]] for i in range(n_images)]

        # Scaling
        if self.synthModel.affine_scaling_range != 0:
            self.transformDictionary['affineScaling'] = self.synthModel.generateAffineScaling(
                n_images)
        else:
            self.transformDictionary['affineScaling'] = [
                np.diag(np.array[1, 1, 1]) for i in range(n_images)]

        # Now combine the affines
        self.transformDictionary['affineTransform'] = self.synthModel.combineAffines(
            self.transformDictionary['affineTranslation'], self.transformDictionary['affineRotation'], self.transformDictionary['affineScaling'])

        # If parameter is not zero, generate downsampling factor
        if self.synthModel.downsample_factor != 0:
            self.transformDictionary['downsampleFactor'] = self.synthModel.generateDownsampleFactor(
                n_images)

        # If parameter is not 0, generate new label intensity mean
        if self.synthModel.label_mean != 0:
            self.transformDictionary['labelIntensityMean'] = self.synthModel.generateLabelIntensityMean(
                n_images)

    def synthImages(self):
        print('Applying affine transforms...' + '\n')

        # If we have label intensity means, we run them through the model
        if len(self.transformDictionary['labelIntensityMean']) != 0:
            self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyLabelIntensityMean(
                self.matrix, self.transformDictionary['labelIntensityMean'], self.transformDictionary['headers'])

        # Have to run the affine transforms no matter what, already set default affines for non-existent parameters
        self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyAffineTransform(
            self.transformDictionary['matrices'], self.transformDictionary['affineTransform'], self.transformDictionary['headers'])

        # If we have downsample factors, downsample all matrices through the model
        if len(self.transformDictionary['downsampleFactor']) != 0:
            self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyDownsampling(
                self.transformDictionary['matrices'], self.transformDictionary['downsampleFactor'], self.transformDictionary['headers'])
        return self.transformDictionary['matrices'], self.transformDictionary['headers']
