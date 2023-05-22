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
        print('Generating affine transforms...')
        self.transformDictionary['headers'] = self.synthModel.copyHeaders(
            self.header, n_images)
        self.transformDictionary['affineTransform'] = self.synthModel.generateAffineTransform(self.affine,
                                                                                              self.header, n_images)
        self.transformDictionary['downsampleFactor'] = self.synthModel.generateDownsampleFactor(
            n_images)
        self.transformDictionary['labelIntensityMean'] = self.synthModel.generateLabelIntensityMean(
            n_images)

    def synthImages(self):
        print('Applying affine transforms...')
        step_1_label_mean_images, step_1_label_mean_headers = self.synthModel.applyLabelIntensityMean(
            self.matrix, self.transformDictionary['labelIntensityMean'], self.transformDictionary['headers'])
        step_2_affine_images, step_2_affine_headers = self.synthModel.applyAffineTransform(
            step_1_label_mean_images, self.transformDictionary['affineTransform'], step_1_label_mean_headers)
        step_3_downsample_images, step_3_downsample_headers = self.synthModel.applyDownsampling(
            step_2_affine_images, self.transformDictionary['downsampleFactor'], step_2_affine_headers)
        return step_3_downsample_images, step_3_downsample_headers
