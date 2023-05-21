# Testing

from data_loader import DataLoader

load_test = DataLoader("Data/InputImages/509_T1w_brain.nii.gz")
print(load_test.imageMatrix)
