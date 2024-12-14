# pylint: disable=too-many-instance-attributes
"""
The single class that stores all data needed to work on a project
"""
import dataclasses

from .action import Action
from .metric import Metric
from .pathway import Pathway
from .scenario import Scenario


@dataclasses.dataclass
class PathwaysProject:
    id: str
    name: str
    organization: str
    start_year: int
    end_year: int
    conditions: list[Metric]
    criteria: list[Metric]
    scenarios: list[Scenario]
    actions: list[Action]
    root_pathway: Pathway
