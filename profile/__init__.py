"""
profile package -- Profile data extraction and AI-powered skill selection.

Exposes the ProfileExtractionOrchestrator and MockProfileProvider as
the primary entry points for loading a person's profile and filtering
it against a target job description.
"""

from profile.mock_provider import MockProfileProvider
from profile.orchestrator import ProfileExtractionOrchestrator

__all__ = ["ProfileExtractionOrchestrator", "MockProfileProvider"]
