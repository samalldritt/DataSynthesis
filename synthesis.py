import numpy as np
from scipy.spatial.transform import Rotation
from scipy.ndimage import affine_transform
from scipy.ndimage import zoom


class SyntheticModel():

    # Eventually want parameters here
    def __init__(self, args):
        """
        SyntheticModel performs the operations on the image class to create synth images

        Input: arguments
        """
        self.args = args

    def copyHeaders(self, header, n_images):
        """
        This function just makes a new header for every image, we change them later when performing actual operations
        """
        new_headers = [header.copy() for _ in range(n_images)]
        return new_headers

    def generateAffineTransform(self, original_affine, header, n_images):
        """
        For all NIFTI data, create new attribute with dictionary with uniformly sampled distributions of each of the affine parameters
        """
        affines = []
        affine_translation_scaling = 1 / header['pixdim'][1]
        for i in range(n_images):
            # Sampling random values for translation, rotation, and scaling
            translation = np.random.uniform(low=0, high=15, size=3)
            scaled_translation = np.multiply(
                translation, affine_translation_scaling)
            rotation_degrees = np.random.uniform(low=0, high=45, size=3)
            rotation_radians = np.radians(rotation_degrees)
            scaling = np.random.uniform(low=0.8, high=1.2, size=3)

            # Create rotation matrices for each axis
            rotation_x = Rotation.from_rotvec(
                rotation_radians[0] * np.array([1, 0, 0]))
            rotation_x_matrix = rotation_x.as_matrix()
            rotation_y = Rotation.from_rotvec(
                rotation_radians[1] * np.array([0, 1, 0]))
            rotation_y_matrix = rotation_y.as_matrix()
            rotation_z = Rotation.from_rotvec(
                rotation_radians[2] * np.array([0, 0, 1]))
            rotation_z_matrix = rotation_z.as_matrix()

            # Create a scaling matrix
            scaling_matrix = np.diag(scaling)

            # Combine the matrices
            init_affine = rotation_x_matrix @ rotation_y_matrix @ rotation_z_matrix @ scaling_matrix
            affine = np.zeros((4, 4))
            affine[:3, :3] = init_affine
            affine[:3, 3] = scaled_translation.ravel()
            affine[3, :] = [0, 0, 0, 1]

            # Add affine to affine list
            affines.append(affine)

        return affines

    def generateDownsampleFactor(self, n_images):
        """
        Uniformly samples downsampling factor from a range and adds to the dictionary of transforms
        """
        print('Generating downsampling factors...')
        downsample_list = []
        for i in range(n_images):
            downsample_factor = np.random.uniform(low=1, high=5)
            downsample_list.append(downsample_factor)

        return downsample_list

    def generateLabelIntensityMean(self, n_images):
        """
        This function generates a list of 'new' label intensity means for each n_images
        """
        print('Generating label intensities...')
        label_intensities = np.random.uniform(low=0.0, high=1.0, size=n_images)
        return label_intensities

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
