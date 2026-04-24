"""Knowledge base: car classes, track types, handling problems, workflow, baseline generators."""

from rf2.knowledge.car_classes import CAR_CLASSES
from rf2.knowledge.track_types import TRACK_TYPES
from rf2.knowledge.problems import HANDLING_PROBLEMS
from rf2.knowledge.workflow import SETUP_WORKFLOW
from rf2.knowledge.baseline import (
    generate_baseline,
    generate_smart_baseline,
    get_problem_recommendations,
)

__all__ = [
    "CAR_CLASSES",
    "TRACK_TYPES",
    "HANDLING_PROBLEMS",
    "SETUP_WORKFLOW",
    "generate_baseline",
    "generate_smart_baseline",
    "get_problem_recommendations",
]
