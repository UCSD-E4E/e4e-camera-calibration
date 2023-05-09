import argparse

from __init__ import __app_name__, __version__
from commands.cli_command import CliCommand
from commands.calibrate_command import CalibrateCommand
from commands.extract_calibration_images import (
    ExtractCalibrationImagesCommand,
)
from commands.tune_disparity_command import TuneDisparityCommand
from commands.version_command import VersionCommand
from commands.rectify_images import RectifyImagesCommand


class Cli:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            prog=__app_name__,
            description="Engineers for Exploration tool for calibrating cameras.",
        )

        self._parser.add_argument(
            "-v",
            "--version",
            help="Displays the version number of the Cli.",
            action="store_true",
        )

        self._subparsers = self._parser.add_subparsers(dest="command")
        self._add_subparser(ExtractCalibrationImagesCommand())
        self._add_subparser(CalibrateCommand())
        self._add_subparser(TuneDisparityCommand())
        self._add_subparser(VersionCommand())
        self._add_subparser(RectifyImagesCommand())

    def _add_subparser(self, command: CliCommand):
        subparser = self._subparsers.add_parser(command.name, help=command.help)
        command.parser = subparser
        subparser.set_defaults(command=command)

    def execute(self):
        args = self._parser.parse_args()

        if args.version:
            print(__version__)
        elif args.command:
            parsed_args = args.command.builder.parse_args(args)
            exit_code = args.command.execute(args, parsed_args) or 0

            if exit_code != 0:
                exit(exit_code)


Cli().execute()
