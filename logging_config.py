"""
logging_config -- Centralized logging configuration for JobSaw.

Sets up dual logging:
1. Console: INFO level, clean and readable formatting.
2. File ('run.log' in the current output directory): DEBUG level,
   verbose formatting for troubleshooting API calls and compilation.
"""

import logging
import os
import sys
from typing import Optional


def setup_logging(output_dir: Optional[str] = None) -> None:
    """Configure root logger with console and optional file handlers.

    Args:
        output_dir: If provided, a detailed 'run.log' will be written here.
    """
    # Reset existing handlers to avoid duplicates during interactive testing
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Base configuration: capture DEBUG and above globally
    logging.root.setLevel(logging.DEBUG)

    # 1. Console Handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_fmt = logging.Formatter(
        "%(asctime)s | %(name)-30s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_fmt)
    logging.root.addHandler(console_handler)

    # 2. File Handler (DEBUG level) -- only if output_dir is specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        log_file = os.path.join(output_dir, "run.log")
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_fmt)
        logging.root.addHandler(file_handler)

    logging.info("Logging initialized.")
    if output_dir:
        logging.info("Detailed logs are being written to: %s", log_file)
