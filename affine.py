import numpy as np
from scipy.spatial.transform import Rotation
from scipy.ndimage import affine_transform
from scipy.ndimage import zoom


class AffineGenerator:

    def __init__(self, header, translation_range, rotation_range, scaling_range, n_images):
        self.header = header
        self.translation_range = translation_range
        self.rotation_range = rotation_range
        self.scaling_range = scaling_range
        self.n_images = n_images

        translations = self.generateAffineTranslation()
        rotations = self.generateAffineRotation()
        scalings = self.generateAffineScaling()
        self.affines = self.combineAffines(translations, rotations, scalings)

    # NEED TO ADD IF TRANSLATION RANGE = 0 (for others too)
    def generateAffineTranslation(self):
        """
        Generate the affine translation portion
        """
        if self.translation_range == 0:
            translations = [np.zeros((3,), dtype=int)
                            for i in range(self.n_images)]
        else:
            translations = []
            affine_translation_scaling = 1 / self.header['pixdim'][1]
            for i in range(self.n_images):
                translation = np.random.uniform(
                    low=0, high=self.translation_range, size=3)
                scaled_translation = np.multiply(
                    translation, affine_translation_scaling)
                translations.append(scaled_translation)

        return translations

    def generateAffineRotation(self):
        """
        Generate the affine rotation portion
        """
        if self.rotation_range == 0:
            rotations = [[np.array[1, 0, 0], np.array[0, 1, 0],
                          np.array[0, 0, 1]] for i in range(self.n_images)]
        else:
            rotations = []
            for i in range(self.n_images):
                rotation_degrees = np.random.uniform(
                    low=0, high=self.rotation_range, size=3)
                rotation_radians = np.radians(rotation_degrees)
                rotation_x = Rotation.from_rotvec(
                    rotation_radians[0] * np.array([1, 0, 0]))
                rotation_x_matrix = rotation_x.as_matrix()
                rotation_y = Rotation.from_rotvec(
                    rotation_radians[1] * np.array([0, 1, 0]))
                rotation_y_matrix = rotation_y.as_matrix()
                rotation_z = Rotation.from_rotvec(
                    rotation_radians[2] * np.array([0, 0, 1]))
                rotation_z_matrix = rotation_z.as_matrix()
                rotation = [rotation_x_matrix,
                            rotation_y_matrix, rotation_z_matrix]
                rotations.append(rotation)

        return rotations

    def generateAffineScaling(self):
        """
        Generate the affine scaling portion
        """
        if self.scaling_range == [100, 100]:
            scalings = [np.diag(np.array[1, 1, 1])
                        for i in range(self.n_images)]
        else:
            scalings = []
            for i in range(self.n_images):
                scaling = np.random.uniform(
                    low=self.scaling_range[0], high=self.scaling_range[1], size=3)
                scaling_matrix = np.diag(scaling)
                scalings.append(scaling_matrix)

        return scalings

    def combineAffines(self, translations, rotations, scalings):
        self.affines = []
        for index, translation in enumerate(translations):
            init = rotations[index][0] @ rotations[index][1] @ rotations[index][2] @ scalings[index]
            affine = np.zeros((4, 4))
            affine[:3, :3] = init
            affine[:3, 3] = translations[index].ravel()
            affine[3, :] = [0, 0, 0, 1]
            self.affines.append(affine)
