import numpy as np
from scipy.spatial.transform import Rotation
from scipy.ndimage import affine_transform
from scipy.ndimage import zoom
import logger


class Affine:

    def __init__(self, images, translation_range, rotation_range, scaling_range, n_images):
        self.logger_instance = logger.setup_logger()
        self.images = images
        self.headers = [image.header for image in images]
        self.translation_range = translation_range
        self.rotation_range = rotation_range
        self.scaling_range = scaling_range
        self.n_images = n_images

        translations = self.generateAffineTranslation(self.images)
        rotations = self.generateAffineRotation(self.images)
        scalings = self.generateAffineScaling(self.images)
        self.affines = self.combineAffines(
            self.images, translations, rotations, scalings)
        self.applyAffines(self.images, self.affines)

    # NEED TO ADD IF TRANSLATION RANGE = 0 (for others too)

    def generateAffineTranslation(self, images):
        """
        Generate the affine translation portion
        """
        for image_index, image in enumerate(images):
            if self.translation_range == 0:
                self.logger_instance.info(
                    f"Generating affine translation for image {image_index + 1} (AFFINE TRANSLATION TURNED OFF)")
                translations = [np.zeros((3,), dtype=int)
                                for i in range(self.n_images)]
                image.transformDict['affineTranslation'] = translations
            else:
                self.logger_instance.info(
                    f"Generating affine translation for image {image_index + 1}")
                affine_translation_scaling = 1 / self.headers[0]['pixdim'][1]
                translations = []
                for i in range(self.n_images):
                    translation = np.random.uniform(
                        low=0, high=self.translation_range, size=3)
                    scaled_translation = np.multiply(
                        translation, affine_translation_scaling)
                    translations.append(scaled_translation)
                image.transformDict['affineTranslation'] = translations

        return translations

    def generateAffineRotation(self, images):
        """
        Generate the affine rotation portion
        """
        for image_index, image in enumerate(images):
            if self.rotation_range == 0:
                self.logger_instance.info(
                    f"Generating affine rotation for image {image_index + 1} (AFFINE ROTATION TURNED OFF)")
                rotations = [
                    np.identity(3) for i in range(self.n_images)]
                image.transformDict['affineRotation'] = rotations
            else:
                rotations = []
                for i in range(self.n_images):
                    self.logger_instance.info(
                        f"Generating affine rotation for synth image {i + 1} for image {image_index + 1}")
                    rotation_degrees = np.random.uniform(
                        low=-self.rotation_range, high=self.rotation_range, size=3)
                    rotation_radians = np.radians(rotation_degrees)
                    rotation_x = np.array([[1, 0, 0],
                                           [0, np.cos(rotation_radians[0]), -
                                          np.sin(rotation_radians[0])],
                                           [0, np.sin(rotation_radians[0]), np.cos(rotation_radians[0])]])

                    rotation_y = np.array([[np.cos(rotation_radians[1]), 0, np.sin(rotation_radians[1])],
                                           [0, 1, 0],
                                           [-np.sin(rotation_radians[1]), 0, np.cos(rotation_radians[1])]])

                    rotation_z = np.array([[np.cos(rotation_radians[2]), -np.sin(rotation_radians[2]), 0],
                                           [np.sin(rotation_radians[2]), np.cos(
                                               rotation_radians[2]), 0],
                                           [0, 0, 1]])

                    rotation_matrix = np.dot(
                        np.dot(rotation_x, rotation_y), rotation_z)
                    rotations.append(rotation_matrix)
                image.transformDict['affineRotation'] = rotations

        return rotations

    def generateAffineScaling(self, images):
        """
        Generate the affine scaling portion
        """
        for image_index, image in enumerate(images):
            if self.scaling_range == [100, 100]:
                self.logger_instance.info(
                    f"Generating affine scaling for image {image_index + 1} (AFFINE SCALING TURNED OFF)")
                scalings = [np.diag(np.array[1, 1, 1])
                            for i in range(self.n_images)]
                image.transformDict['affineScaling'] = scalings
            else:
                scalings = []
                for i in range(self.n_images):
                    self.logger_instance.info(
                        f"Generating affine scaling for synth image {i + 1} for image {image_index + 1}")
                    scaling = np.random.uniform(
                        low=self.scaling_range[0], high=self.scaling_range[1], size=3)
                    scaling_matrix = np.diag(scaling)
                    scalings.append(scaling_matrix)

                image.transformDict['affineScaling'] = scalings

        return scalings

    def combineAffines(self, images, translations, rotations, scalings):
        for image_index, image in enumerate(images):
            self.affines = []
            for index, translation in enumerate(translations):
                self.logger_instance.info(
                    f"Combining affines for synth image {index + 1} for image {image_index + 1}")
                init = rotations[index] @ scalings[index]
                affine = np.zeros((4, 4))
                affine[: 3, : 3] = init
                affine[: 3, 3] = translations[index].ravel()
                affine[3, :] = [0, 0, 0, 1]
                self.affines.append(affine)
            image.transformDict['affineTransform'] = self.affines

        return self.affines

    def applyAffines(self, images, affines):
        for image_index, image in enumerate(images):
            self.logger_instance.info(
                f"Applying affines for image {image_index + 1}")
            image.transformDict['matrices'] = np.array([affine_transform(
                image.transformDict['matrices'][i], affines[i]) for i in range(len(image.transformDict['matrices']))])
            image.transformDict['newAffines'] = affines
