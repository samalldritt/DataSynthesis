# DataSynthesis
In development project that will synthesize new fMRI data by randomizing parameters from a chosen uniform distribution and applying to an original dataset.
A current problem in the neuoroimaging field is the time, expense, and scarce resources / subjects available for obtaining high quality data, leading to inconsistent analyses.
With this in mind, this project aims to synthesize new data that has the same core features of 'real' structural and functional MRI data, but creating potentially infinite variations by sampling parameters from a chosen distribution.

I frequently work with non-human primate fMRI data, and use machine learning models to mask the brain and extract valuable information. A problem, however, is the lack of non-human primate data to adequately train a CNN model to generalizably perform this task. Site, gender, and age effects are significantly changing a multitude of features about the brain that make it difficult to use a 'one-size-fits-all' model. With this project, I aim to solve this problem by providing a potentially infinite amount of data to a commonly used U-Net to train a generalizable CNN brain extraction model.

## The parameters:
- Affine:
  - Translation
  - Rotation
  - Scaling
- Non-linear deformations (warps)
- Mean / standard deviation of voxel intensity normalization
- Downsample factor
- Cropping (mm)


