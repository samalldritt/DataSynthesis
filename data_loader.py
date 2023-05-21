import nibabel as nib
import numpy as np


class DataLoader:

    def __init__(self, image_path):
        self.image_path = image_path

    def load(self):
        self.image = nib.load(self.image_path)
        self.imageMatrix = self.image.get_fdata()
        self.imageHeader = self.image.header
