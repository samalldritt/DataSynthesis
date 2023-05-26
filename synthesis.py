import numpy as np
from scipy.spatial.transform import Rotation
from scipy.ndimage import affine_transform
from scipy.ndimage import zoom
from affine import AffineGenerator
from deformation import DeformationGenerator
import SimpleITK as sitk
import utils


class SyntheticModel():

    # Eventually want parameters here
    def __init__(self, args):
        """
        SyntheticModel performs the operations on the image class to create synth images

        Input: arguments
        """
        if args != None:
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

    def applyDeformationFields(self, matrices, deformations):
        print('Applying deformation fields...' + '\n')
        new_matrices = []
        for index, matrix in enumerate(matrices):
            original_image = sitk.GetImageFromArray(matrix)
            deformation_array = deformations[index]
            deformation_field = sitk.GetImageFromArray(deformation_array)

            deformation_field.SetDirection(original_image.GetDirection())
            deformation_field.SetSpacing(original_image.GetSpacing())
            deformation_field.SetOrigin(original_image.GetOrigin())

            deformation_transform = sitk.DisplacementFieldTransform(
                deformation_field)

            # Generate a regular grid of points
            grid = sitk.GridSource(
                outputPixelType=sitk.sitkUInt8,
                size=original_image.GetSize(),
                sigma=[0.0] * original_image.GetDimension(),
                spacing=original_image.GetSpacing(),
                origin=original_image.GetOrigin())

            # Convert the grid points to physical space coordinates
            grid_points = [grid.TransformIndexToPhysicalPoint(
                index) for index in np.ndindex(original_image.GetSize())]

            # Apply the deformation field to the grid points
            deformed_points = [deformation_transform.TransformPoint(
                point) for point in grid_points]

            # Create a new grid by transforming the deformed points back to index space
            deformed_grid = sitk.Image(
                original_image.GetSize(), sitk.sitkVectorFloat64)
            for index, point in zip(np.ndindex(original_image.GetSize()), deformed_points):
                deformed_grid.SetPixel(index, point)

            # Resample the original image using the deformed grid
            resampled_image = sitk.Resample(
                original_image, deformed_grid, sitk.sitkBSpline)

            print('Resampled image size:', resampled_image.GetSize())

            resampled_image_array = sitk.GetArrayFromImage(resampled_image)
            new_matrices.append(resampled_image_array)

        return new_matrices

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
