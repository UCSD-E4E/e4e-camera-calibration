from argparse import ArgumentParser, Namespace
from argument_parser_builder import ArgumentParserBuilder, ParsedArguments

from commands.cli_command import CliCommand
from cameras.calibrated_stereo_camera import (
    CalibratedStereoCamera,
)

import os
import cv2

class RectifyImagesCommand(CliCommand):
    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return "rectify-images"

    @property
    def help(self) -> str:
        return "Given a dataset of unrectified pairs and the cameras stereo map, rectify all image pairs."
    
    def execute(self, args: Namespace, parsed_arguments: ParsedArguments):
        calibrated_camera = CalibratedStereoCamera(parsed_arguments.camera)
        calibrated_camera.load_calibration(args.calibration_tables)

        #Loop over all scenes
        for scene in os.listdir(args.dataset_dir):
            if not os.path.isdir(os.path.join(args.dataset_dir, scene)):
                continue
            
            unrectified_dir = os.path.join(args.dataset_dir, scene, 'unrectified')
            if not os.path.isdir(unrectified_dir):
                continue
            rectified_dir = os.path.join(args.dataset_dir, scene, 'rectified')
            if not os.path.isdir(rectified_dir):
                os.makedirs(rectified_dir)
                continue

            im0_path = os.path.join(unrectified_dir, 'im0.png')
            im1_path = os.path.join(unrectified_dir, 'im1.png')
            if not os.path.exists(im0_path) or not os.path.exists(im1_path):
                continue

            left_unrect = cv2.imread(im0_path)
            right_unrect = cv2.imread(im1_path)

            left_rect, right_rect = calibrated_camera.rectify_images(left_unrect, right_unrect)
            left_rect = cv2.cvtColor(left_rect, cv2.COLOR_RGB2BGR)
            right_rect = cv2.cvtColor(right_rect, cv2.COLOR_RGB2BGR)

            left_rect_path = os.path.join(rectified_dir, 'im0.png')
            right_rect_path = os.path.join(rectified_dir, 'im1.png')

            cv2.imwrite(left_rect_path, left_rect)
            cv2.imwrite(right_rect_path, right_rect)


    def _set_parser(self, parser: ArgumentParser, builder: ArgumentParserBuilder):
        builder.add_camera_parameters()

        parser.add_argument(
            "-t",
            "--calibration-tables",
            type=str,
            required=True,
            help="The calibration tables generated from the calibrate command.",
        )

        parser.add_argument(
            "--dataset-dir",
            type=str,
            required=True,
            help="Directory of the images for calibration."
        )