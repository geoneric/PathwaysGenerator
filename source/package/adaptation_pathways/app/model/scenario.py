# pylint: disable=too-many-return-statements,too-many-branches
from .metric import MetricValue, MetricValueState


class YearDataPoint:
    def __init__(self, year: int):
        self.year = year
        self.metric_data: dict[str, MetricValue] = {}

    def get_or_add_data(self, metric_id: str) -> MetricValue:
        data = self.metric_data.get(metric_id, None)
        if data is None:
            data = MetricValue(0, MetricValueState.ESTIMATE)
            self.metric_data[metric_id] = data
        return data


class Scenario:
    def __init__(self, scenario_id: str, name: str):
        self.id = scenario_id
        self.name = name
        self.yearly_data: list[YearDataPoint] = []

    def get_or_add_year(self, year: int) -> YearDataPoint:
        data = self.get_data(year)
        if data is None:
            data = YearDataPoint(year)
            self.yearly_data.append(data)
            self.sort_yearly_data()

        return data

    def get_data(self, year: int) -> YearDataPoint | None:
        for data_point in self.yearly_data:
            if data_point.year == year:
                return data_point
        return None

    def set_data(self, year: int, metric_id: str, value: MetricValue):
        data = self.get_or_add_year(year)
        data.metric_data[metric_id] = value

    def sort_yearly_data(self):
        self.yearly_data.sort(key=lambda point: point.year)

    def recalculate_values(self, metric_id: str):
        for index, data in enumerate(self.yearly_data):
            metric_value = data.get_or_add_data(metric_id)

            # We only recalculate estimated values
            if not metric_value.is_estimate:
                continue

            previous_point = self._get_previous_value(index, metric_id)
            next_point = self._get_next_value(index, metric_id)

            # If we don't have any data to interpolate, we can't recalculate
            if previous_point is None and next_point is None:
                continue

            # If we have both a previous and next point, we can interpolate
            if previous_point is not None and next_point is not None:
                metric_value.value = self._estimate_value(
                    data.year,
                    previous_point[0],
                    previous_point[1].value,
                    next_point[0],
                    next_point[1].value,
                )
                continue

            # If we don't have a previous point, try extrapolating with the next two points
            if next_point is not None:
                # Check if we have a second data point
                second_next_point = self._get_next_value(next_point[2], metric_id)

                # If we don't have a second next data point, we have to use the next one as is
                if second_next_point is None:
                    metric_value.value = next_point[1].value
                    continue

                # Otherwise we can extrapolate
                metric_value.value = self._estimate_value(
                    data.year,
                    next_point[0],
                    next_point[1].value,
                    second_next_point[0],
                    second_next_point[1].value,
                )
                continue

            # If we don't have a next point, try extrapolating with the previous two points
            if previous_point is not None:
                # Check if we have a second data point
                second_previous_point = self._get_previous_value(
                    previous_point[2], metric_id
                )

                # If we don't have a second next data point, we have to use the next one as is
                if second_previous_point is None:
                    metric_value.value = previous_point[1].value
                    continue
                # Otherwise we can extrapolate
                metric_value.value = self._estimate_value(
                    data.year,
                    second_previous_point[0],
                    second_previous_point[1].value,
                    previous_point[0],
                    previous_point[1].value,
                )

    def _get_previous_value(
        self, year_index: int, metric_id: str
    ) -> tuple[int, MetricValue, int] | None:
        for index in range(year_index - 1, -1, -1):
            data = self.yearly_data[index]
            metric_value = data.metric_data[metric_id]
            if not metric_value.is_estimate:
                return (data.year, metric_value, index)
        return None

    def _get_next_value(
        self, year_index: int, metric_id: str
    ) -> tuple[int, MetricValue, int] | None:
        for index in range(year_index + 1, len(self.yearly_data)):
            data = self.yearly_data[index]
            metric_value = data.metric_data[metric_id]
            if not metric_value.is_estimate:
                return (data.year, metric_value, index)

        return None

    def _estimate_value(
        self, x: float, x_1: float, y_1: float, x_2: float, y_2: float
    ) -> float:
        slope = (y_2 - y_1) / (x_2 - x_1)
        return slope * (x - x_1) + y_1

    def estimate_tipping_point(self, metric_id: str, metric_value: float) -> float:
        if len(self.yearly_data) == 0:
            return 0

        if len(self.yearly_data) == 1:
            return self.yearly_data[0].year

        # Find the global min and max to establish the bounds
        global_min: tuple[float, float] = (0, 0)
        has_global_min = False
        global_max: tuple[float, float] = (0, 0)
        has_global_max = False

        for year_data in self.yearly_data:
            year_value = year_data.metric_data.get(metric_id, None)
            if year_value is None:
                continue

            if not has_global_min or year_value.value < global_min[1]:
                has_global_min = True
                global_min = (year_data.year, year_value.value)

            if not has_global_max or year_value.value > global_max[1]:
                has_global_max = True
                global_max = (year_data.year, year_value.value)

        # That means we don't have any valid data points for this metric
        if not has_global_min or not has_global_max:
            return 0

        if metric_value <= global_min[1]:
            return global_min[0]

        if metric_value >= global_max[1]:
            return global_max[0]

        for index, year_data in enumerate(self.yearly_data):
            if index + 1 >= len(self.yearly_data):
                continue

            year_value = year_data.metric_data.get(metric_id, None)
            if year_value is None:
                continue

            next_year_data = self.yearly_data[index + 1]
            next_year_value = next_year_data.metric_data.get(metric_id, None)

            if next_year_value is None:
                continue

            min_year, min_value, max_year, max_value = (
                (
                    year_data.year,
                    year_value.value,
                    next_year_data.year,
                    next_year_value.value,
                )
                if year_value.value <= next_year_value.value
                else (
                    next_year_data.year,
                    next_year_value.value,
                    year_data.year,
                    year_value.value,
                )
            )

            if metric_value < min_value or metric_value > max_value:
                continue

            return self._estimate_value(
                metric_value, min_value, float(min_year), max_value, float(max_year)
            )

        # We should never get here, but just in case
        return 0
