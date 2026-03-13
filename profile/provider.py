"""
provider -- Abstract base class for profile data sources.

Defines the ProfileProvider interface (Strategy Pattern) so that
concrete implementations (mock, API-backed, scraper-backed) can be
swapped without modifying any agent or orchestrator code.
"""

from abc import ABC, abstractmethod

from profile.models import ProfileData


class ProfileProvider(ABC):
    """Interface for retrieving a person's profile data.

    Subclass this and implement `get_profile` to supply data from
    any source (hard-coded mock, database, REST API, web scraper, etc.).
    """

    @abstractmethod
    def get_profile(self) -> ProfileData:
        """Return the full profile for the target person.

        Returns:
            ProfileData instance populated with all available sections.
        """
        ...
