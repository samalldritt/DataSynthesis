import numpy as np
from scipy.spatial.transform import Rotation
from scipy.ndimage import affine_transform
from scipy.ndimage import zoom
from affine import AffineGenerator
from deformation import DeformationGenerator
import utils


class SyntheticModel():

    # Eventually want parameters here
    def __init__(self, args):
        """
        SyntheticModel performs the operations on the image class to create synth images

        Input: arguments
        """
        self.affine_translation_range = args['affine_translation']
        self.affine_rotation_range = args['affine_rotation']
        self.affine_scaling_range = [
            (100 - args['affine_scaling']) / 100, (100 + args['affine_scaling']) / 100]
        self.downsample_factor = args['downsample_factor']
        self.label_mean = args['mean_label_intensity']
        self.deformation_resolution = args['deformation_resolution']
        self.deformation_sd = args['deformation_sd']
        self.n_images = args['n_images']

    def copyMatrices(self, matrix):
        """
        Copies the matrices and adds it to the transform dictionary
        """
        matrices = []
        for i in range(self.n_images):
            matrices.append(matrix)

        return matrices

    def copyHeaders(self, header):
        """
        This function just makes a new header for every image, we change them later when performing actual operations
        """
        new_headers = [header.copy() for _ in range(self.n_images)]
        return new_headers

    def generateAffines(self, header):
        affineGenerator = AffineGenerator(
            header, self.affine_translation_range, self.affine_rotation_range, self.affine_scaling_range, self.n_images)
        return affineGenerator.affines

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

    def generateLabelIntensityMean(self):
        """
        This function generates a list of 'new' label intensity means for each n_images
        """
        print('Generating label intensities...')
        label_intensities = np.random.uniform(
            low=0.0, high=1.0, size=self.n_images)
        return label_intensities

    def generateDeformationFields(self, header):
        deformer = DeformationGenerator(
            self.deformation_resolution, self.deformation_sd, self.n_images, header)
        return deformer.deformation_fields

    def applyAffineTransform(self, matrices, affines, headers):
        """
        Applies affines in the transform dictionary to the image matrix to return new sets of image matrices for each affine

        Input: original matrix, list of affines

        Output: new matrix for each affine transform
        """
        new_matrices = []
        new_headers = []
        for index, matrix in enumerate(matrices):
            # Adjusting the NIFTI information
            new_data = affine_transform(matrix, affines[index])
            new_matrices.append(np.array(new_data))

            # Adjusting the header information (for now it is the exact same as the input)
            new_header = headers[index]
            new_headers.append(new_header)

        return new_matrices, new_headers

    def applyDownsampling(self, matrices, downsampling, headers):
        """
        Applying the downsampling factors from the downsampling dictionary to a list of matrices from step 1 (affine transformation)
        """
        print('Applying downsampling...')
        new_matrices = []
        new_headers = []
        for index, matrix in enumerate(matrices):

            # Adjusting the nifti image first
            downsampled_data = zoom(
                matrix, 1/downsampling[index], order=0)
            new_matrices.append(downsampled_data)

            # Correcting the header information
            # Changing the pixdims
            new_header = headers[index]
            new_header['pixdim'][1:4] = new_header['pixdim'][1:4] * \
                downsampling[index]
            # Changing the dim
            new_header['dim'][1:4] = downsampled_data.shape
            new_headers.append(new_header)

        return new_matrices, new_headers

    def applyLabelIntensityMean(self, matrices, label_intensity_means, headers):
        """
        This function is for changing the label intensity means for each matrix passed
        """
        print('Changing label intensity means...')
        new_matrices = []
        new_headers = []
        for index, matrix in enumerate(matrices):
            # Adjusting the nifti data
            scaled_data = (matrix - np.mean(matrix)) / (2 * np.std(matrix))
            scaled_data = scaled_data + \
                (label_intensity_means[index] - np.mean(scaled_data))
            new_matrices.append(scaled_data)

            # Adjusting the header information (if any correction needed)
            new_header = headers[index]
            new_headers.append(new_header)

        return new_matrices, new_headers
