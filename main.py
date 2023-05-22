from data_holder import DataHolder
from synthesis import SyntheticModel
import sys
import os

# Testing


def cycleData():
    """
    Cycles and loads all data from the base directory
    """
    print('Reading input...')
    path = os.path.join(os.getcwd(), 'Data', 'InputImages')
    niftiFilePaths = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.nii.gz'):
                niftiFilePaths.append(os.path.join(root, filename))

    return niftiFilePaths


def main():
    inputNiftiPaths = cycleData()
    synthModel = SyntheticModel('args')
    dataHolder = DataHolder(inputNiftiPaths, synthModel)
    dataHolder.makeTransforms(1)
    dataHolder.applyTransforms()


if __name__ == '__main__':
    main()


# In main class, should have a way to pass the arguments into a dictionary to pass to synthesis model
