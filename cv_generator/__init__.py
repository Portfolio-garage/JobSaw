"""
cv_generator package -- E2E pipeline for generating tailored LaTeX CVs.

Exposes the CvGenerationOrchestrator which combines profile extraction
with AI-powered LaTeX template filling and PDF compilation.
"""

from cv_generator.orchestrator import CvGenerationOrchestrator

__all__ = ["CvGenerationOrchestrator"]
