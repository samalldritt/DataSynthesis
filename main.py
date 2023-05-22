from data_loader import DataLoader
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
    dataLoader = DataLoader(inputNiftiPaths)
    print(dataLoader.images[0]['ImageMatrix'])


if __name__ == '__main__':
    main()


# Need to have a function that loops through all data in input directory and runs through

# In main class, should have a way to pass the arguments into a dictionary to pass to synthesis model
