import io
import re

from ..action import Action
from ..action_combination import ActionCombination
from .conversion import sequences_to_sequence_graph
from .sequence_graph import SequenceGraph


edition_pattern = r"\d+"
action_name_pattern = r"\w+"


def _open_stream(pathname: str | io.IOBase) -> io.IOBase:
    stream: io.IOBase

    if isinstance(pathname, str):
        stream = open(pathname, encoding="utf-8")  # pylint: disable=consider-using-with
    else:
        stream = pathname

    return stream


# pylint: disable-next=too-many-locals
def read_tipping_points(
    tipping_points_pathname: str | io.IOBase, actions: list[Action]
) -> dict[Action, int]:
    stream = _open_stream(tipping_points_pathname)
    tipping_point_by_name_and_edition: dict[tuple[str, int], int] = {}

    tipping_point_pattern = r"(?P<tipping_point>\d+)"
    action_pattern = (
        rf"(?P<action_name>{action_name_pattern})(\[(?P<edition>{edition_pattern})\])?"
    )
    pattern = rf"{action_pattern}\s+{tipping_point_pattern}"

    with stream:
        for line in stream:
            # Strip comments and surrounding white space
            line_as_string = str(line).split("#", 1)[0].strip()

            # Skip empty lines
            if len(line_as_string) > 0:
                match = re.fullmatch(pattern, line_as_string)

                if match is None:
                    raise ValueError(f"Cannot parse tipping point: {line_as_string}")

                action_name = match.group("action_name")
                edition = (
                    int(match.group("edition"))
                    if match.group("edition") is not None
                    else 0
                )
                tipping_point = int(match.group("tipping_point"))

                if (action_name, edition) in tipping_point_by_name_and_edition:
                    raise ValueError(
                        f"Multiple tipping points found for action {action_name}[{edition}]"
                    )

                tipping_point_by_name_and_edition[(action_name, edition)] = (
                    tipping_point
                )

    tipping_point_by_action: dict[Action, int] = {}

    for (name, edition), tipping_point in tipping_point_by_name_and_edition.items():
        for action in actions:
            if action.name == name and action.edition == edition:
                tipping_point_by_action[action] = tipping_point
                break

    return tipping_point_by_action


def _conditionally_add_node(
    name: str, edition: int, action_by_name_and_edition: dict[tuple[str, int], Action]
):
    if (name, edition) not in action_by_name_and_edition:
        action = Action(name, edition)
        action_by_name_and_edition[(name, edition)] = action


# pylint: disable-next=too-many-locals
def _parse_sequences(
    line: str,
    action_by_name_and_edition: dict[tuple[str, int], Action],
) -> tuple[Action, Action]:
    from_action_pattern = (
        rf"(?P<from_action_name>{action_name_pattern})"
        rf"(\[(?P<from_edition>{edition_pattern})\])?"
    )
    # TODO Allow any number of actions to be combined(?)
    to_action_pattern = (
        rf"(?P<to_action_name>{action_name_pattern})"
        rf"(\[(?P<to_edition>{edition_pattern})\])?"
        rf"(\(\s*(?P<action1_name>{action_name_pattern})"
        rf"(\[(?P<edition1>{edition_pattern})\])?\s*&\s*"
        rf"(?P<action2_name>{action_name_pattern})"
        rf"(\[(?P<edition2>{edition_pattern})\])?\s*\))?"
    )
    pattern = rf"{from_action_pattern}\s+{to_action_pattern}"

    match = re.fullmatch(pattern, line)

    if match is None:
        raise ValueError(f"Cannot parse sequence: {line}")

    from_action_name = match.group("from_action_name")
    from_edition = (
        int(match.group("from_edition"))
        if match.group("from_edition") is not None
        else 0
    )

    _conditionally_add_node(
        from_action_name,
        from_edition,
        action_by_name_and_edition,
    )

    to_action_name = match.group("to_action_name")
    to_edition = (
        int(match.group("to_edition")) if match.group("to_edition") is not None else 0
    )
    action1_name = match.group("action1_name") or ""
    edition1 = (
        int(match.group("edition1")) if match.group("edition1") is not None else 0
    )
    action2_name = match.group("action2_name") or ""
    edition2 = (
        int(match.group("edition2")) if match.group("edition2") is not None else 0
    )

    assert (action1_name == "" and action2_name == "") or (
        action1_name != "" and action2_name != ""
    )
    combine_actions = action1_name != ""

    if (
        to_action_name,
        to_edition,
    ) not in action_by_name_and_edition:
        if not combine_actions:
            action = Action(to_action_name, to_edition)
            action_by_name_and_edition[(to_action_name, to_edition)] = action
        else:
            _conditionally_add_node(
                action1_name,
                edition1,
                action_by_name_and_edition,
            )
            _conditionally_add_node(
                action2_name,
                edition2,
                action_by_name_and_edition,
            )

            action1 = action_by_name_and_edition[(action1_name, edition1)]
            action2 = action_by_name_and_edition[(action2_name, edition2)]

            action = ActionCombination(to_action_name, [action1, action2], to_edition)
            action_by_name_and_edition[(to_action_name, to_edition)] = action
    else:
        # In case of action combinations, the first occurrence of the action must
        # define which actions are combined
        if combine_actions:
            raise ValueError("Action combinations must be defined ASAP and only once")

    from_action = action_by_name_and_edition[(from_action_name, from_edition)]
    to_action = action_by_name_and_edition[(to_action_name, to_edition)]

    return from_action, to_action


def read_sequences(sequences_pathname: str | io.IOBase) -> list[tuple[Action, Action]]:
    """
    Read sequences of actions from a stream and return a list with the actions

    :param sequences_pathname: Pathname of file to read from or an open stream to read from

    Comments are supported: everything after the first pound sign (#) on a line is
    skipped. Example::

        # Diverging sequences
        current a
        current b
        current c  # Third sequence
        # Done specifying sequences
    """
    stream = _open_stream(sequences_pathname)
    sequences: list[tuple[Action, Action]] = []
    action_by_name_and_edition: dict[tuple[str, int], Action] = {}

    with stream:
        for line in stream:
            # Strip comments and surrounding white space
            line_as_string = str(line).split("#", 1)[0].strip()

            # Skip empty lines
            if len(line_as_string) > 0:
                from_action, to_action = _parse_sequences(
                    line_as_string,
                    action_by_name_and_edition,
                )
                sequences.append((from_action, to_action))

    return sequences


def action_level_by_first_occurrence(
    sequences: list[tuple[Action, Action]]
) -> dict[Action, float]:
    """
    Determine a level per action the sequences of actions passed in

    The returned collection of levels can be used for vertically ordering actions in graphs. The
    levels are based on the order in which the actions are mentioned in the input collection.
    Actions occurring earlier in the collection, are assigned lower levels.
    """
    level_by_action: dict[Action, float] = {}

    for idx, (from_action, to_action) in enumerate(sequences, 1):
        if from_action not in level_by_action:
            level_by_action[from_action] = idx + 0.01
        if to_action not in level_by_action:
            level_by_action[to_action] = idx - 0.01

    return level_by_action


def read_sequence_graph(sequences_pathname: str | io.IOBase) -> SequenceGraph:
    sequences = read_sequences(sequences_pathname)
    sequence_graph = sequences_to_sequence_graph(sequences)

    return sequence_graph
