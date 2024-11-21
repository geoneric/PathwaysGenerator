from metric import Metric
from action import Action, ActionDependency
from pathway import Pathway
from scenario import Scenario

class PathwaysProject:
    id: str
    name: str
    organization: str
    start_year: int
    end_year: int
    conditions: list[Metric]
    criteria: list[Metric]
    actions: list[Action]
    action_dependencies: list[ActionDependency]
    pathways: list[Pathway]
    scenarios: list[Scenario]
