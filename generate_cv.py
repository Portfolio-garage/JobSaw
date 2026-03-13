"""
generate_cv.py -- CLI entry point for end-to-end CV generation.

Reads a raw job description, loads the mock profile, invokes the full
generation pipeline (analysis, selection, LaTeX generation, compilation),
and writes all results to a timestamped output directory.

Usage:
    python generate_cv.py tests/sample_job_description.txt
"""

import sys

# Crucial hack: Create the output directory upfront so we can pass
# it into the logging config before any modules do `import logging`.
import datetime
import os
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUT_DIR = os.path.join(os.getcwd(), "output", timestamp)

from logging_config import setup_logging
# Initialize logging before importing the orchestrators!
setup_logging(output_dir=OUT_DIR)

import logging
from cv_generator.orchestrator import CvGenerationOrchestrator
from profile.mock_provider import MockProfileProvider

logger = logging.getLogger("main")


def _read_input() -> str:
    """Read job description text from a file argument or stdin."""
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                return fh.read()
        except FileNotFoundError:
            logger.error("File not found: %s", filepath)
            sys.exit(1)
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        print(
            "Usage: python generate_cv.py <job_description.txt>\n"
            "       or pipe text via stdin.",
            file=sys.stderr,
        )
        sys.exit(1)


# Custom log filter to stop logs from stepping on our spinner stdout
class SpinnerFilter(logging.Filter):
    def __init__(self, spinner):
        self.spinner = spinner

    def filter(self, record):
        if self.spinner.is_running:
            # Clear spinner line before logging
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
        return True


class Spinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.is_running = False
        self._thread = None

    def start(self):
        import threading
        self.is_running = True
        self._thread = threading.Thread(target=self._spin)
        self._thread.daemon = True
        self._thread.start()

    def _spin(self):
        import time
        import sys
        chars = "|/-\\"
        idx = 0
        while self.is_running:
            sys.stdout.write(f"\r{chars[idx]} {self.message}")
            sys.stdout.flush()
            idx = (idx + 1) % len(chars)
            time.sleep(0.1)

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread.join()
        sys.stdout.write('\r\033[K') # clear line
        sys.stdout.flush()


def main() -> None:
    """Run the complete CV generation process."""
    job_text = _read_input()

    if not job_text.strip():
        logger.error("Empty job description provided.")
        sys.exit(1)

    # Data Source & Template Path
    provider = MockProfileProvider()
    template_path = os.path.join("templates", "cv_template.tex")

    if not os.path.exists(template_path):
        logger.error("Template not found at: %s", template_path)
        sys.exit(1)

    orchestrator = CvGenerationOrchestrator(
        provider=provider,
        template_path=template_path
    )

    # Monkey-patch the orchestrator's output directory so it matches our logger dir
    orchestrator._create_output_dir = lambda: OUT_DIR

    spinner = Spinner("Running AI Pipeline (this may take a few minutes)...")
    
    # Attach filter to console handler to prevent messy log overlap
    for handler in logging.root.handlers:
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
            handler.addFilter(SpinnerFilter(spinner))

    try:
        print(f"\nPipeline started. Detailed logs written to: {OUT_DIR}\\run.log")
        spinner.start()
        pdf_path = orchestrator.run(job_text)
        spinner.stop()
        
        print("\n" + "#" * 60)
        print("  CV GENERATION SUCCESSFUL")
        print("#" * 60)
        print(f"\nYour CV has been compiled and saved to:\n{pdf_path}\n")
        print(f"All intermediate data (JSON, .tex) and logs are in:\n{OUT_DIR}\n")
    except Exception as e:
        spinner.stop()
        logger.exception("Pipeline failed. Check run.log for full details.")
        print("\n" + "!" * 60)
        print("  PIPELINE ERROR")
        print("!" * 60)
        print(f"\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
