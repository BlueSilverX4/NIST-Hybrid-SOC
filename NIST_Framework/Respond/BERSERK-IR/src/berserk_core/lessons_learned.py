from dataclasses import dataclass


@dataclass
class LessonsLearned:
    case_id: str
    status: str
    what_worked: list[str]
    what_failed: list[str]
    detection_source: list[str]
    early_detection: list[str]
    playbook_effectiveness: list[str]
    detection_tuning: list[str]
    defensive_improvements: list[str]


def assess_lessons(case) -> LessonsLearned:

    return LessonsLearned(
        case_id=case.case_id,
        status="LESSONS_RECORDED",

        what_worked=[
            "SSH brute-force detection identified repeated authentication failures.",
            "Threat scoring identified the activity as high risk.",
            "The decision gate prevented automatic containment.",
            "The response plan was generated in simulation mode.",
            "Recovery and closure assessments were completed.",
        ],

        what_failed=[
            "No confirmed detection or response failure was identified.",
        ],

        detection_source=[
            "Repeated SSH authentication failures generated the security finding.",
            "The same source IP targeted both admin and root accounts.",
        ],

        early_detection=[
            "Earlier detection cannot be established from the available evidence.",
        ],

        playbook_effectiveness=[
            "The Black Swordsman Incident Response Protocol provided structured investigation and response guidance.",
            "The playbook mapped the investigation to Phase 4 — Apostle Hunt.",
        ],

        detection_tuning=[
            "Review authentication-failure thresholds and detection logic.",
            "Evaluate whether repeated targeting of privileged accounts should increase detection priority.",
        ],

        defensive_improvements=[
            "Evaluate additional SSH authentication protections.",
            "Continue monitoring authentication activity targeting privileged accounts.",
            "Consider stronger controls for repeated authentication failures.",
        ],
    )
