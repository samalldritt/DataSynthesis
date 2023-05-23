# This file creates a class called 'image' that contains data about a loaded NIFTI image
# Will also import functions from synthesis that creates synthetic images and adds to this class

from synthesis import SyntheticModel
import numpy as np


class Image:

    def __init__(self, imageMatrix, imageHeader, affine, transformDictionary, synthModel):
        self.matrix = imageMatrix
        self.header = imageHeader
        self.affine = affine
        self.transformDictionary = transformDictionary
        self.synthModel = synthModel

    def synthTransforms(self, n_images):
        print('Generating affine transforms...' + '\n')

        # Make copies of matrix
        self.transformDictionary['matrices'] = self.synthModel.copyMatrices(
            self.matrix)

        # Make copies of headers
        self.transformDictionary['headers'] = self.synthModel.copyHeaders(
            self.header)

        self.transformDictionary['deformationFields'] = self.synthModel.generateDeformationFields(
            self.header)

        # create the affines
        self.transformDictionary['affineTransform'] = self.synthModel.generateAffines(
            self.header)

        # If parameter is not zero, generate downsampling factor
        if self.synthModel.downsample_factor != 0:
            self.transformDictionary['downsampleFactor'] = self.synthModel.generateDownsampleFactor(
            )

        # If parameter is not 0, generate new label intensity mean
        if self.synthModel.label_mean != 0:
            self.transformDictionary['labelIntensityMean'] = self.synthModel.generateLabelIntensityMean(
            )

    def synthImages(self):
        print('Applying affine transforms...' + '\n')

        # If we have label intensity means, we run them through the model
        if len(self.transformDictionary['labelIntensityMean']) != 0:
            self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyLabelIntensityMean(
                self.transformDictionary['matrices'], self.transformDictionary['labelIntensityMean'], self.transformDictionary['headers'])

        # Have to run the affine transforms no matter what, already set default affines for non-existent parameters
        self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyAffineTransform(
            self.transformDictionary['matrices'], self.transformDictionary['affineTransform'], self.transformDictionary['headers'])

        # If we have downsample factors, downsample all matrices through the model
        if len(self.transformDictionary['downsampleFactor']) != 0:
            self.transformDictionary['matrices'], self.transformDictionary['headers'] = self.synthModel.applyDownsampling(
                self.transformDictionary['matrices'], self.transformDictionary['downsampleFactor'], self.transformDictionary['headers'])

        return self.transformDictionary['matrices'], self.transformDictionary['headers']
