import numpy as np
import SimpleITK as sitk
import utils


class DeformationGenerator:

    def __init__(self, displacement_resolution, sd, n_images, header):
        self.sd = sd
        self.image_resolution = header['pixdim'][1]
        self.image_shape = header['dim'][1:4]
        print(self.image_shape)
        self.displacement_resolution = utils.scale_mm(
            displacement_resolution, self.image_resolution)
        self.n_images = n_images
        self.header = header

        self.displacement_vectors = self.generateDisplacementVectors()
        self.deformation_fields = self.vectorIntegration(
            self.displacement_vectors)

    def generateDisplacementVectors(self):
        displacement_vectors = []
        for i in range(self.n_images):
            displacement_sd = self.displacement_resolution / np.sqrt(self.sd)
            displacement_vector = np.random.normal(
                scale=displacement_sd, size=(3, *self.image_shape))
            displacement_vectors.append(displacement_vector)

        return displacement_vectors

    def vectorIntegration(self, displacement_vectors):
        deformation_fields = []
        for i in range(len(displacement_vectors)):
            displacement_field = sitk.GetImageFromArray(
                displacement_vectors[i])
            deformation_transform = sitk.DisplacementFieldTransform(
                displacement_field)
            for i in range(5):
                deformation_transform = sitk.CompositeTransform(
                    [deformation_transform])
            deformation_field = sitk.TransformToDisplacementField(
                deformation_transform)
            deformation_field = sitk.Resample(
                deformation_field, self.image_shape, sitk.Transform(), sitk.sitkBSpline)
            deformation_array = sitk.GetArrayFromImage(deformation_field)
            deformation_fields.append(deformation_array)

        return deformation_fields
