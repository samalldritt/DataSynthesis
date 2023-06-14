from data_holder import DataHolder
from synthesis import SyntheticModel
import logger
import time
import argparse
import sys
import os


def main(**kwargs):
    if kwargs != None:
        logger_instance = logger.setup_logger()
        logger_instance.info('Starting synthetic data generation...')
        logger.log_parameters(logger_instance, **kwargs)
        synthModel = SyntheticModel(kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Synthetic data builder for NIFTI images')

    parser.add_argument('-i',
                        type=str,
                        help='Enter input directory for images',
                        required=True)
    parser.add_argument('-o',
                        type=str,
                        help='Enter output directory for images',
                        required=True)
    parser.add_argument('--affine_translation',
                        type=int,
                        choices=range(0, 26),
                        default=25,
                        help='Customize range to affine translation range (in mm) from 0 to n (default: 15)')
    parser.add_argument('--affine_rotation',
                        type=int,
                        choices=range(0, 46),
                        default=45,
                        help='Set affine rotation parameter (in degrees) from 0 to n (default: 45)')
    parser.add_argument('--affine_scaling',
                        type=int,
                        choices=range(0, 30),
                        default=20,
                        help='Set distance from 100 percent for affine scaling (20 = 80-120)')
    parser.add_argument('--downsample_factor',
                        type=int,
                        choices=range(0, 11),
                        default=5,
                        help='Set the range from 1 as the downsampling factor')
    parser.add_argument('--mean_label_intensity',
                        type=int,
                        choices=[0],
                        help='Turn off label normalization (0)')
    parser.add_argument('--n_images',
                        type=int,
                        default=10,
                        help='Set the amount of synthetic images to generate')
    parser.add_argument('--deformation_resolution',
                        type=int,
                        choices=range(8, 17),
                        default=10,
                        help='Set the resolution of the displacement warp')
    parser.add_argument('--deformation_sd',
                        type=int,
                        choices=range(1, 4),
                        default=3,
                        help='Set the standard deviation of the randomly generated displacement warp')

    args = parser.parse_args()

    main(**vars(args))
