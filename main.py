from data_holder import DataHolder
from synthesis import SyntheticModel
import sys
import os

# Testing


def cycleData():
    """
    Cycles and loads all data from the base directory
    """
    path = os.path.join(os.getcwd(), 'Data')
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
    dataHolder.runSynth(50)


if __name__ == '__main__':
    main()


# In main class, should have a way to pass the arguments into a dictionary to pass to synthesis model
