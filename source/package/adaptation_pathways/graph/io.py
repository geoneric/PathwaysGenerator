import io
import re

from .node import Action, ActionCombination
from .sequence_graph import SequenceGraph


def _open_stream(pathname: str | io.IOBase) -> io.IOBase:
    stream: io.IOBase

    if isinstance(pathname, str):
        stream = open(pathname, encoding="utf-8")  # pylint: disable=consider-using-with
    else:
        stream = pathname

    return stream


def read_tipping_points(
    tipping_points_pathname: str | io.IOBase, actions: list[Action]
) -> dict[Action, int]:
    stream = _open_stream(tipping_points_pathname)
    tipping_point_by_label: dict[str, int] = {}

    with stream:
        for line in stream:
            line_as_string = str(line.strip())  # Keep mypy happy

            if len(line_as_string) > 0 and not line_as_string.startswith("#"):
                label, tipping_point_as_string = line_as_string.strip().split()
                tipping_point = int(tipping_point_as_string)  # Keep mypy happy
                tipping_point_by_label[label] = int(tipping_point)

    tipping_point_by_action: dict[Action, int] = {}

    # Multiple actions can have the same label. Assign the same tipping point to all of them.
    for label, tipping_point in tipping_point_by_label.items():
        for action in actions:
            if action.label == label:
                tipping_point_by_action[action] = tipping_point

    return tipping_point_by_action


# pylint: disable-next=too-many-locals
def read_sequences(sequences_pathname: str | io.IOBase) -> SequenceGraph:
    """
    Read sequences from a stream and return the resulting graph

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
    sequence_graph = SequenceGraph()

    version_pattern = r"\[\d+\]"
    action_pattern = r"\w+"

    from_action_pattern = (
        rf"(?P<from_action>{action_pattern})(?P<from_version>{version_pattern})?"
    )
    to_action_pattern = (
        rf"(?P<to_action>{action_pattern})(?P<to_version>{version_pattern})?"
        rf"(\(\s*(?P<action1>{action_pattern})(?P<version1>{version_pattern})?\s*&\s*"
        rf"(?P<action2>{action_pattern})(?P<version2>{version_pattern})?\s*\))?"
    )
    sequence_pattern = rf"{from_action_pattern}\s+{to_action_pattern}"

    action_by_name: dict[str, Action] = {}

    with stream:
        for line in stream:
            # Strip comments and surrounding white space
            line_as_string = str(line).split("#", 1)[0].strip()

            # Skip empty lines
            if len(line_as_string) > 0:
                match = re.fullmatch(sequence_pattern, line_as_string)

                if match is None:
                    raise ValueError(f"Cannot parse sequence: {line_as_string}")

                from_action_name = match.group("from_action")
                # from_version = match.group("from_version")

                if from_action_name not in action_by_name:
                    action_by_name[from_action_name] = Action(from_action_name)

                to_action_name = match.group("to_action")
                # to_version = match.group("to_version")
                action1_name = match.group("action1") or ""
                # version1 = match.group("version1")
                action2_name = match.group("action2") or ""
                # version2 = match.group("version2")

                assert (action1_name == "" and action2_name == "") or (
                    action1_name != "" and action2_name != ""
                )
                combine_actions = action1_name != ""

                if to_action_name not in action_by_name:
                    if not combine_actions:
                        action_by_name[to_action_name] = Action(to_action_name)
                    else:
                        if action1_name not in action_by_name:
                            action_by_name[action1_name] = Action(action1_name)
                        if action2_name not in action_by_name:
                            action_by_name[action2_name] = Action(action2_name)

                        action1 = action_by_name[action1_name]
                        action2 = action_by_name[action2_name]

                        action_by_name[to_action_name] = ActionCombination(
                            to_action_name, action1, action2
                        )
                else:
                    # In case of action combinations, the first occurrence of the action must
                    # define which actions are combined
                    if combine_actions:
                        raise ValueError(
                            "Action combinations must be defined ASAP and only once"
                        )

                from_action = action_by_name[from_action_name]
                to_action = action_by_name[to_action_name]

                sequence_graph.add_sequence(from_action, to_action)

    return sequence_graph
