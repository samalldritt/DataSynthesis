import numpy as np
import logger


class LabelIntensity():

    def __init__(self, images):
        self.logger_instance = logger.setup_logger()
        self.images = images
        self.n_images = self.images[0].n_images
        self.generateLabelIntensityMean()
        self.applyLabelIntensityMean(self.images)

    def generateLabelIntensityMean(self):
        """
        This function generates a list of 'new' label intensity means for each n_images
        """
        self.logger_instance.info('Generating label intensity means...')
        label_intensities = np.random.uniform(
            low=0.0, high=1.0, size=(len(self.images), self.n_images))
        for index, image in enumerate(self.images):
            image.transformDict['labelIntensityMean'] = np.array([
                label_intensity for label_intensity in label_intensities[index]])

    def scaleData(self, matrix):
        return (matrix - np.mean(matrix)) / (2 * np.std(matrix))

    def applyLabelIntensityMean(self, images):
        for index, image in enumerate(images):
            self.logger_instance.info(
                'Applying label intensity means for image ' + str(index + 1))
            imageMatrices = image.transformDict['matrices']
            imageIntensityMeans = image.transformDict['labelIntensityMean']
            image.transformDict['matrices'] = [self.scaleData(
                imageMatrices[i] + (imageIntensityMeans[i] - np.mean(self.scaleData(imageMatrices[i])))) for i in range(len(imageMatrices))]
            print(np.amax(image.transformDict['matrices'][0]))
