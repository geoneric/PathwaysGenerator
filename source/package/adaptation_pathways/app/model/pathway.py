import dataclasses
from typing import Iterator

from .action import Action
from .metric import Metric, MetricValue


@dataclasses.dataclass
class Pathway:
    id: str
    last_action: Action
    metric_data: dict[Metric, MetricValue | None] | None = None
    children: list["Pathway"] | None = None

    @classmethod
    def get_id(cls, ancestors: list["Pathway"], new_action: Action):
        ids = [pathway.last_action.id for pathway in ancestors]
        ids.append(new_action.id)
        return "->".join(ids)

    def __hash__(self):
        return self.id.__hash__()

    def all_children(self):
        if self.children is None:
            return

        for child in self.children:
            yield child
            yield from child.all_children()

    def self_and_all_children(self):
        yield self
        yield from self.all_children()

    def all_paths(
        self, base_path: list["Pathway"] | None = None
    ) -> Iterator[tuple["Pathway", list["Pathway"]]]:

        path = [self] if base_path is None else base_path + [self]

        yield (self, path)

        if self.children is None:
            return

        for child in self.children:
            yield from child.all_paths(path)

    def all_child_paths(
        self, base_path: list["Pathway"] | None = None
    ) -> Iterator[tuple["Pathway", list["Pathway"]]]:
        path = [self] if base_path is None else base_path + [self]

        if self.children is None:
            return

        for child in self.children:
            yield from child.all_paths(path)

    def get_value(self, metric: Metric) -> MetricValue | None:
        if self.metric_data is None:
            return None

        return self.metric_data.get(metric)

    def get_formatted_value(self, metric: Metric) -> str:
        if self.metric_data is None:
            return ""

        data = self.metric_data.get(metric)
        if data is None:
            return ""

        return metric.unit.format(data.value)
