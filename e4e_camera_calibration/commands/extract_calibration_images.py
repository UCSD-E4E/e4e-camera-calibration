import os
from argparse import ArgumentParser, Namespace
from glob import glob

from e4e_camera_calibration.argument_parser_builder import (
    ArgumentParserBuilder,
    ParsedArguments,
)
from e4e_camera_calibration.calibrators.calibrator import Calibrator
from e4e_camera_calibration.calibrators.stereo_calibrator import StereoCalibrator
from e4e_camera_calibration.commands.cli_command import CliCommand


class ExtractCalibrationImagesCommand(CliCommand):
    def __init__(self):
        super().__init__()

    @property
    def help(self) -> str:
        return "Extracts calibration images from a specified video."

    @property
    def name(self) -> str:
        return "extract-calibration-images"

    def execute(self, args: Namespace, parsed_arguments: ParsedArguments):
        # Prep the directory to receive the new calibration images.
        os.makedirs(args.output, exist_ok=True)
        for file in glob(f"{args.output}/{args.prefix}*.png"):
            os.unlink(file)

        camera = parsed_arguments.camera
        camera.load(args.input)

        calibrator: Calibrator = None
        if camera.number_of_sensors == 2:
            calibrator = StereoCalibrator(camera)
        else:
            raise NotImplementedError()

        calibrator.generate_calibration_images(args.output, args.prefix)

    def _set_parser(self, parser: ArgumentParser, builder: ArgumentParserBuilder):
        builder.add_camera_parameters()

        parser.add_argument(
            "-i",
            "--input",
            required=True,
            help="The video file to pull calibration images from.",
        )

        parser.add_argument(
            "-o",
            "--output",
            required=True,
            help="Where to save the calibration images.",
        )

        parser.add_argument(
            "-p",
            "--prefix",
            default="",
            help="The prefix to use when naming the calibration images.",
        )
