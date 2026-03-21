#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import subprocess

import rich_click as click
import click_completion

click_completion.init()

from sequana_pipetools.options import *
from sequana_pipetools import SequanaManager

NAME = "multicov"

help = init_click(
    NAME,
    groups={
        "Pipeline Specific": [
            "--annotation-file",
            "--reference-file",
            "--circular",
            "--double-threshold",
            "--high-threshold",
            "--low-threshold",
            "--mixture-models",
            "--window",
            "--chunksize",
            "--binning",
            "--cnv-clustering",
        ],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory=NAME)
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions, input_pattern="*.bed", add_input_readtag=False)
@include_options_from(ClickGeneralOptions)
@click.option("--annotation-file", default=None, help="Genbank file to annotate detected events")
@click.option("--reference-file", default=None, help="Genome reference FASTA file used to plot GC content")
@click.option("--circular", is_flag=True, help="Set if the genome is circular")
@click.option("--double-threshold", default=0.5, show_default=True, help="Double threshold for clustering")
@click.option("--high-threshold", default=4.0, show_default=True, help="High threshold for ROI detection")
@click.option("--low-threshold", default=-4.0, show_default=True, help="Low threshold for ROI detection")
@click.option(
    "--mixture-models",
    default=2,
    show_default=True,
    help="Number of mixture models. Set to 1 or 3 in rare occasions",
)
@click.option(
    "--window",
    default=20000,
    show_default=True,
    help="Running median window size. Keep at 20000 to detect CNV up to 10kb",
)
@click.option("--chunksize", default=5000000, show_default=True, help="Chunk size for large genomes")
@click.option("--binning", default=-1, show_default=True, help="Bin size for large genomes (-1 to disable)")
@click.option(
    "--cnv-clustering", default=-1, show_default=True, help="Merge events closer than this distance (-1 to disable)"
)
def main(**options):
    manager = SequanaManager(options, NAME)
    options = manager.options

    manager.setup()

    if options.from_project is None:
        cfg = manager.config.config

        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern

        cfg.sequana_coverage.circular = options.circular
        cfg.sequana_coverage.double_threshold = options.double_threshold
        cfg.sequana_coverage.high_threshold = options.high_threshold
        cfg.sequana_coverage.low_threshold = options.low_threshold
        cfg.sequana_coverage.mixture_models = options.mixture_models
        cfg.sequana_coverage.window_size = options.window
        cfg.sequana_coverage.chunksize = options.chunksize
        cfg.sequana_coverage.binning = options.binning
        cfg.sequana_coverage.cnv_clustering = options.cnv_clustering

        if options.annotation_file:
            annotation = os.path.abspath(options.annotation_file)
            if not os.path.exists(annotation):
                raise IOError(f"{options.annotation_file} not found")
            cfg.sequana_coverage.annotation_file = annotation

        if options.reference_file:
            reference = os.path.abspath(options.reference_file)
            if not os.path.exists(reference):
                raise IOError(f"{options.reference_file} not found")
            cfg.sequana_coverage.reference_file = reference

    manager.teardown()


if __name__ == "__main__":
    main()
