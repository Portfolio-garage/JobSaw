"""
compiler -- LaTeX-to-PDF compilation via pdflatex subprocess.

Writes the generated LaTeX source to a .tex file, invokes pdflatex
to compile it, and returns the path to the resulting PDF.
Requires MiKTeX or TeX Live installed with pdflatex on PATH.
"""

import logging
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)


class LatexCompiler:
    """Compiles a LaTeX source string into a PDF file.

    Uses pdflatex via subprocess. The compilation runs twice to
    resolve cross-references (standard LaTeX practice).
    """

    def __init__(self) -> None:
        self._pdflatex = shutil.which("pdflatex")
        if not self._pdflatex:
            logger.warning(
                "pdflatex not found on PATH. PDF compilation will fail. "
                "Install MiKTeX (https://miktex.org/download) or TeX Live."
            )

    def compile(self, tex_path: str, output_dir: str) -> str:
        """Compile a .tex file to PDF.

        Args:
            tex_path: Absolute path to the .tex source file.
            output_dir: Directory where the PDF will be written.

        Returns:
            Absolute path to the generated PDF file.

        Raises:
            RuntimeError: If pdflatex is not installed or compilation fails.
        """
        if not self._pdflatex:
            raise RuntimeError(
                "pdflatex is not installed or not on PATH. "
                "Install MiKTeX (https://miktex.org/download) or TeX Live."
            )

        logger.info("Compiling LaTeX: %s", tex_path)
        logger.info("Output directory: %s", output_dir)

        # pdflatex arguments: non-interactive, output to specified dir.
        cmd = [
            self._pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-disable-installer", # Prevent MiKTeX from popping up UI dialogues
            f"-output-directory={output_dir}",
            tex_path,
        ]
        logger.debug("pdflatex command: %s", " ".join(cmd))

        # Run twice to resolve cross-references.
        for run_number in (1, 2):
            logger.info("pdflatex pass %d/2...", run_number)
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                logger.error("pdflatex stderr:\n%s", result.stderr)
                logger.error("pdflatex stdout (last 2000 chars):\n%s", result.stdout[-2000:])
                raise RuntimeError(
                    f"pdflatex failed on pass {run_number} with return code "
                    f"{result.returncode}. Check the log for details."
                )
            logger.debug("pdflatex pass %d stdout (last 500 chars): %s", run_number, result.stdout[-500:])

        # Derive the PDF filename from the .tex filename.
        tex_basename = os.path.splitext(os.path.basename(tex_path))[0]
        pdf_path = os.path.join(output_dir, f"{tex_basename}.pdf")

        if not os.path.exists(pdf_path):
            raise RuntimeError(
                f"PDF file not found after compilation: {pdf_path}"
            )

        # Clean up auxiliary files (.aux, .log, .out) from pdflatex.
        for ext in (".aux", ".log", ".out"):
            aux_file = os.path.join(output_dir, f"{tex_basename}{ext}")
            if os.path.exists(aux_file):
                os.remove(aux_file)
                logger.debug("Cleaned up: %s", aux_file)

        logger.info("PDF compiled successfully: %s", pdf_path)
        return pdf_path
