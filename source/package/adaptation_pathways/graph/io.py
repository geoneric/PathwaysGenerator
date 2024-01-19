import io
import re

from .node import Action
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
    sequence_pattern = r"(?P<from_action>\w+) (?P<to_action>\w+)"
    action_by_name: dict[str, Action] = {}

    with stream:
        for line in stream:
            # Strip comments and surrounding white space
            line_as_string = str(line).split("#", 1)[0].strip()

            # Skip empty lines
            if len(line_as_string) > 0:
                match = re.fullmatch(sequence_pattern, line_as_string)

                if match is None:
                    raise ValueError("Could not parse sequence: {line_as_string}")

                from_action_specification = match.group("from_action")
                to_action_specification = match.group("to_action")

                from_action_name = from_action_specification
                to_action_name = to_action_specification

                if from_action_name not in action_by_name:
                    action_by_name[from_action_name] = Action(from_action_name)

                if to_action_name not in action_by_name:
                    action_by_name[to_action_name] = Action(to_action_name)

                from_action = action_by_name[from_action_name]
                to_action = action_by_name[to_action_name]

                sequence_graph.add_sequence(from_action, to_action)

    return sequence_graph
