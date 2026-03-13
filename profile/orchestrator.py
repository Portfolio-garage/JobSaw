"""
orchestrator -- Coordinates profile extraction and AI skill selection.

Takes a ProfileProvider and a job description, runs the existing
JobAnalysisOrchestrator, then feeds both the profile and the job
analysis to the SkillsSelectorAgent to produce curated CV data.
"""

import json
import logging
from typing import Tuple

from agents.models import JobAnalysis
from agents.orchestrator import JobAnalysisOrchestrator
from profile.models import ProfileData, SelectedProfileData
from profile.provider import ProfileProvider
from profile.skills_selector_agent import SkillsSelectorAgent

logger = logging.getLogger(__name__)


class ProfileExtractionOrchestrator:
    """Top-level coordinator for the profile extraction pipeline.

    Usage:
        from profile.mock_provider import MockProfileProvider

        orchestrator = ProfileExtractionOrchestrator(MockProfileProvider())
        result = orchestrator.run(raw_job_text)
        print(result.model_dump_json(indent=2))
    """

    def __init__(self, provider: ProfileProvider) -> None:
        """Initialize with a concrete profile data source.

        Args:
            provider: Any ProfileProvider implementation (mock, API, etc.).
        """
        self._provider = provider
        self._job_orchestrator = JobAnalysisOrchestrator()
        self._selector = SkillsSelectorAgent()

    def run(
        self, job_description: str, out_dir: str = None
    ) -> Tuple[SelectedProfileData, ProfileData, JobAnalysis]:
        """Execute the full pipeline: job analysis + profile selection.

        Steps:
            1. Load profile data from the configured provider.
            2. Analyze the job description via the existing agent pipeline.
            3. Pass both to the SkillsSelectorAgent for intelligent filtering.

        Args:
            job_description: Raw job listing text.
            out_dir: Optional directory to stream intermediate results to.

        Returns:
            SelectedProfileData with only job-relevant profile items.
        """
        import time
        import os

        logger.info("Loading profile data...")
        t0 = time.time()
        profile: ProfileData = self._provider.get_profile()
        profile_json = json.dumps(profile.model_dump(), indent=2)
        logger.info("Profile loaded in %.2fs: %s", time.time() - t0, profile.name)

        if out_dir:
            with open(os.path.join(out_dir, "01_profile_data.json"), "w", encoding="utf-8") as f:
                f.write(profile_json)

        logger.info("Running job analysis pipeline...")
        t0 = time.time()
        job_analysis = self._job_orchestrator.analyze(job_description)
        job_analysis_json = json.dumps(job_analysis.model_dump(), indent=2)
        logger.info("Job analysis complete in %.2fs.", time.time() - t0)

        if out_dir:
            with open(os.path.join(out_dir, "02_job_analysis.json"), "w", encoding="utf-8") as f:
                f.write(job_analysis_json)

        logger.info("Running skill selection...")
        t0 = time.time()
        selected = self._selector.select(profile_json, job_analysis_json)
        logger.info("Skill selection complete in %.2fs.", time.time() - t0)

        if out_dir:
            with open(os.path.join(out_dir, "03_selected_profile.json"), "w", encoding="utf-8") as f:
                f.write(json.dumps(selected.model_dump(), indent=2))

        return selected, profile, job_analysis
