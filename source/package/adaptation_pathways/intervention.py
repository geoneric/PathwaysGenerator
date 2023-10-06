class Intervention:
    _description: str
    _tipping_point: float

    def __init__(self, description: str, tipping_point: float) -> None:
        if tipping_point <= 0:
            raise ValueError(f"Invalid, non-positive, tipping point {tipping_point}")

        self._description = description
        self._tipping_point = tipping_point

    @property
    def description(self) -> str:
        return self._description

    @property
    def tipping_point(self) -> float:
        return self._tipping_point


# Policy action or pathway table

# id
# colour
# description
# action or pathway
# type of pathway
# condition tipping

# Condition-based:
# There is some aspect (e.g. sediment deposition, x-axis in pathways plot)
# Conditions refer to this aspect. They tip at x sediment deposition.

# Tipping point settings:
# min_value (float)
# max_value (float)
# show tipping conditions axis (boolean)
# x-axis caption (string)
# ticks x-axis (int)


# Define pathways:
# first action(s) from actions table
# followed by other action from actions table
# method: combine | sequence
# → Note that "current situation" is special. You can't combine with it.
# → Also, you can't make combinations with the same action.
# → Tipping point of pathway has to be updated. This be done automatically, right? Just take
#   the tipping point of the second action.


# Scenarios
# - high sedimentation
# - low sedimentation

# Attach a time-scale to each scenario:
# - Given start year, sedimentation rate is fixed
# - End year: sedimentation rate can be assigned
# Automatically interpolate values


# Time based pathways plot
# - series of pathways plots, for a number of scenarios, against a common time period
# - "Navigability of river decreases over time unless policy actions are taken"
# - Action table: only diff is time instead of condition tipping point
# - Define x-axis:
#     - min value
#     - max value
#     - show tipping point axis
#     - x-axis caption
#     - nr ticks
