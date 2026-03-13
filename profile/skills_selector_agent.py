"""
skills_selector_agent -- AI agent that selects relevant profile items for a job.

Takes a full ProfileData and a JobAnalysis, uses the LLM to determine
which skills, experience, and connections are relevant, and returns
a curated SelectedProfileData.
"""

import json
import logging

from agents.config import get_llm
from profile.models import SelectedProfileData
from profile.prompts import SKILLS_SELECTOR_PROMPT

logger = logging.getLogger(__name__)


class SkillsSelectorAgent:
    """Specialized agent for selecting job-relevant profile items.

    Cross-references the candidate's full profile against a structured
    job analysis to produce a curated subset suitable for CV generation.
    """

    def __init__(self) -> None:
        self._llm = get_llm(temperature=0.0)
        self._chain = SKILLS_SELECTOR_PROMPT | self._llm

    def select(
        self,
        profile_json: str,
        job_analysis_json: str,
    ) -> SelectedProfileData:
        """Run the selection chain and return curated profile data.

        Args:
            profile_json: JSON string of the full ProfileData.
            job_analysis_json: JSON string of the JobAnalysis output
                               from the job description pipeline.

        Returns:
            SelectedProfileData with only the relevant items.
        """
        logger.info("Running SkillsSelectorAgent...")
        response = self._chain.invoke(
            {
                "profile_json": profile_json,
                "job_analysis_json": job_analysis_json,
            }
        )
        raw = response.content.strip()

        # Strip markdown code fences if the model added them anyway.
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0].strip()

        data = json.loads(raw)
        result = SelectedProfileData(**data)
        logger.info("SkillsSelectorAgent complete.")
        return result
