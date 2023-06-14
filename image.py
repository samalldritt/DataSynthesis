# This file creates a class called 'image' that contains data about a loaded NIFTI image
# Will also import functions from synthesis that creates synthetic images and adds to this class

import nibabel as nib
import numpy as np
import logger
import os


class Image:

    def __init__(self, inputImagePath, synthModel, n_images):
        self.logger_instance = logger.setup_logger()
        self.inputImagePath = inputImagePath
        self.synthModel = synthModel
        self.n_images = n_images
        self.matrix, self.affine, self.header = self.loadData(
            self.inputImagePath)
        self.transformDict = self.initializeTransformDict()

    def loadData(self, filePath):
        self.logger_instance.info(
            f"Loading data from {os.path.join(os.getcwd(), filePath)}")
        data = nib.load(filePath)
        matrix = data.get_fdata()
        affine = data.affine
        header = data.header
        return matrix, affine, header

    def initializeTransformDict(self):

        transforms = {
            'matrices': [],
            'affines': [],
            'newAffines': [],
            'headers': [],
            'deformationFields': [],
            'affineTranslation': [],
            'affineRotation': [],
            'affineScaling': [],
            'affineTransform': [],
            'downsampleFactor': [],
            'labelIntensityMean': []
        }

        transforms['matrices'] = [
            self.matrix for i in range(self.n_images)]
        transforms['affines'] = [
            self.affine for i in range(self.n_images)]
        transforms['headers'] = [
            self.header for i in range(self.n_images)]

        return transforms

    def __repr__(self):
        print(self.transformDict)
