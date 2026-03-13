"""
profile_main.py -- CLI entry point for the profile extraction pipeline.

Reads a raw job description, loads the mock profile, runs the AI
skill selector, and prints both the full profile and the curated
selection as formatted output.

Usage:
    python profile_main.py <path_to_job_description.txt>
    cat job.txt | python profile_main.py
"""

import json
import logging
import sys

from profile.mock_provider import MockProfileProvider
from profile.orchestrator import ProfileExtractionOrchestrator


def _read_input() -> str:
    """Read job description text from a file argument or stdin.

    Returns:
        Raw job description text.

    Raises:
        SystemExit: If no input is provided.
    """
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                return fh.read()
        except FileNotFoundError:
            print(f"Error: File not found -- {filepath}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        print(
            "Usage: python profile_main.py <job_description.txt>\n"
            "       or pipe text via stdin.",
            file=sys.stderr,
        )
        sys.exit(1)


def _print_section(title: str, items) -> None:
    """Pretty-print a labelled section to stdout."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    if isinstance(items, list):
        for item in items:
            print(f"  - {item}")
        if not items:
            print("  (none)")
    elif isinstance(items, str):
        print(f"  {items}")


def main() -> None:
    """Run the full profile extraction pipeline and display results."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)-35s | %(levelname)s | %(message)s",
    )

    job_text = _read_input()

    if not job_text.strip():
        print("Error: Empty job description.", file=sys.stderr)
        sys.exit(1)

    # Use mock provider for development; swap with a real provider later.
    provider = MockProfileProvider()
    orchestrator = ProfileExtractionOrchestrator(provider)

    selected, profile, job_analysis = orchestrator.run(job_text)

    # --- Full profile summary ---
    print("\n" + "#" * 60)
    print("  CANDIDATE PROFILE")
    print("#" * 60)
    print(f"\n  Name: {profile.name}")
    print(f"  Summary: {profile.summary}")
    print(f"  Total Skills: {len(profile.skills)}")
    print(f"  Experience Entries: {len(profile.experience)}")
    print(f"  Certifications: {len(profile.certifications)}")
    print(f"  Connections: {len(profile.connections)}")

    # --- AI-selected items ---
    print("\n" + "#" * 60)
    print("  AI-SELECTED PROFILE DATA (for this job)")
    print("#" * 60)

    _print_section("Selected Hard Skills", selected.selected_hard_skills)
    _print_section("Selected Soft Skills", selected.selected_soft_skills)
    _print_section("Selected Experience", selected.selected_experience)
    _print_section("Selected Certifications", selected.selected_certifications)
    _print_section("Selected Connections", selected.selected_connections)
    _print_section("Relevance Rationale", selected.relevance_rationale)

    # --- Raw JSON output ---
    print(f"\n{'=' * 60}")
    print("  RAW JSON -- Selected Profile Data")
    print(f"{'=' * 60}")
    print(json.dumps(selected.model_dump(), indent=2))


if __name__ == "__main__":
    main()
