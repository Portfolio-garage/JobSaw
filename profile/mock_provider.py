"""
mock_provider -- Hard-coded mock profile for development and testing.

Implements ProfileProvider with a realistic developer profile containing
a mix of relevant and irrelevant skills so the AI selector agent has
meaningful choices to make.
"""

from profile.models import (
    ProfileCertification,
    ProfileConnection,
    ProfileData,
    ProfileEducation,
    ProfileExperience,
    ProfileSkill,
)
from profile.provider import ProfileProvider


class MockProfileProvider(ProfileProvider):
    """Returns a hard-coded, realistic developer profile.

    The mock profile intentionally includes skills and experience
    that do NOT match typical job postings (e.g. game development,
    embedded systems) alongside mainstream full-stack skills, so
    the AI selector has non-trivial filtering work to do.
    """

    def get_profile(self) -> ProfileData:
        """Return the pre-built mock profile.

        Returns:
            ProfileData with a comprehensive developer profile.
        """
        return ProfileData(
            name="Alex Johnson",
            summary=(
                "Full-stack software engineer with 7 years of experience building "
                "web applications, REST APIs, and cloud-native services. Passionate "
                "about clean architecture, developer tooling, and mentoring junior "
                "engineers. Also dabbles in game development and embedded systems "
                "as personal hobbies."
            ),
            skills=[
                # -- Relevant full-stack skills --
                ProfileSkill(name="Python", proficiency="Advanced", years=6),
                ProfileSkill(name="JavaScript", proficiency="Advanced", years=7),
                ProfileSkill(name="TypeScript", proficiency="Advanced", years=4),
                ProfileSkill(name="React", proficiency="Advanced", years=5),
                ProfileSkill(name="Node.js", proficiency="Advanced", years=5),
                ProfileSkill(name="PostgreSQL", proficiency="Advanced", years=5),
                ProfileSkill(name="MongoDB", proficiency="Intermediate", years=3),
                ProfileSkill(name="Docker", proficiency="Advanced", years=4),
                ProfileSkill(name="Kubernetes", proficiency="Intermediate", years=2),
                ProfileSkill(name="AWS", proficiency="Advanced", years=4),
                ProfileSkill(name="GraphQL", proficiency="Intermediate", years=2),
                ProfileSkill(name="Redis", proficiency="Intermediate", years=3),
                ProfileSkill(name="Git", proficiency="Expert", years=7),
                ProfileSkill(name="CI/CD", proficiency="Advanced", years=4),
                ProfileSkill(name="Django", proficiency="Advanced", years=4),
                ProfileSkill(name="REST API Design", proficiency="Expert", years=6),
                # -- Soft skills --
                ProfileSkill(name="Team Leadership", proficiency="Advanced", years=3),
                ProfileSkill(name="Mentoring", proficiency="Advanced", years=4),
                ProfileSkill(name="Agile / Scrum", proficiency="Advanced", years=5),
                ProfileSkill(name="Technical Writing", proficiency="Intermediate", years=3),
                ProfileSkill(name="Public Speaking", proficiency="Beginner", years=1),
                # -- Less relevant / niche skills --
                ProfileSkill(name="Unity3D", proficiency="Intermediate", years=2),
                ProfileSkill(name="C#", proficiency="Intermediate", years=2),
                ProfileSkill(name="Arduino / Embedded C", proficiency="Beginner", years=1),
                ProfileSkill(name="Blender 3D", proficiency="Beginner", years=1),
                ProfileSkill(name="Rust", proficiency="Beginner", years=1),
                ProfileSkill(name="MATLAB", proficiency="Beginner", years=1),
            ],
            experience=[
                ProfileExperience(
                    title="Senior Software Engineer",
                    company="CloudScale Inc.",
                    duration="Mar 2022 - Present",
                    description=(
                        "Lead a team of 5 engineers building a multi-tenant SaaS "
                        "analytics platform. Designed microservices architecture on "
                        "AWS (ECS, Lambda, RDS). Reduced API latency by 40% through "
                        "Redis caching and query optimization."
                    ),
                    technologies=[
                        "Python", "TypeScript", "React", "Node.js",
                        "PostgreSQL", "Redis", "AWS", "Docker", "Kubernetes",
                        "GraphQL", "GitHub Actions",
                    ],
                ),
                ProfileExperience(
                    title="Software Engineer",
                    company="WebForge Studios",
                    duration="Jun 2019 - Feb 2022",
                    description=(
                        "Built and maintained e-commerce platforms serving 50k+ "
                        "daily users. Implemented payment integrations (Stripe, "
                        "PayPal) and real-time inventory management. Migrated "
                        "legacy monolith to microservices."
                    ),
                    technologies=[
                        "JavaScript", "React", "Node.js", "Express",
                        "MongoDB", "PostgreSQL", "Docker", "Jenkins",
                    ],
                ),
                ProfileExperience(
                    title="Junior Developer",
                    company="StartupHub",
                    duration="Jan 2018 - May 2019",
                    description=(
                        "Developed internal tools and dashboards using Django and "
                        "React. Wrote unit and integration tests. Participated in "
                        "daily standups and sprint planning."
                    ),
                    technologies=[
                        "Python", "Django", "JavaScript", "React",
                        "PostgreSQL", "Git",
                    ],
                ),
                ProfileExperience(
                    title="Freelance Game Developer",
                    company="Self-Employed",
                    duration="2016 - 2017",
                    description=(
                        "Created two indie mobile games using Unity3D and C#. "
                        "Published on Google Play with a combined 10k+ downloads. "
                        "Handled all aspects: design, programming, and marketing."
                    ),
                    technologies=["Unity3D", "C#", "Blender 3D", "Photoshop"],
                ),
            ],
            education=[
                ProfileEducation(
                    degree="B.Sc. Computer Science",
                    institution="University of Technology",
                    year=2017,
                ),
            ],
            certifications=[
                ProfileCertification(
                    name="AWS Certified Solutions Architect - Associate",
                    issuer="Amazon Web Services",
                    year=2023,
                ),
                ProfileCertification(
                    name="Certified Kubernetes Application Developer (CKAD)",
                    issuer="The Linux Foundation",
                    year=2022,
                ),
                ProfileCertification(
                    name="Unity Certified Developer",
                    issuer="Unity Technologies",
                    year=2017,
                ),
            ],
            connections=[
                ProfileConnection(
                    name="Sarah Chen",
                    title="Engineering Manager",
                    company="CloudScale Inc.",
                    relationship="Manager",
                ),
                ProfileConnection(
                    name="David Park",
                    title="Senior DevOps Engineer",
                    company="CloudScale Inc.",
                    relationship="Colleague",
                ),
                ProfileConnection(
                    name="Maria Garcia",
                    title="CTO",
                    company="WebForge Studios",
                    relationship="Former Manager",
                ),
                ProfileConnection(
                    name="James Wilson",
                    title="Lead Game Designer",
                    company="Riot Games",
                    relationship="Industry Contact",
                ),
                ProfileConnection(
                    name="Prof. Elena Kovacs",
                    title="CS Department Head",
                    company="University of Technology",
                    relationship="Academic Mentor",
                ),
            ],
        )
