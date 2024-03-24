import io
import re
from pathlib import Path

from .. import alias
from ..action import Action
from ..action_combination import ActionCombination
from ..graph.io import action_name_pattern, edition_pattern, open_stream
from ..plot.colour import hex_to_rgba


def format_actions_path(basename_pathname: str) -> Path:
    """
    Return path formatted as `<name>-action.txt`
    """
    return Path(f"{basename_pathname}-action.txt")


def format_sequences_path(basename_pathname: str) -> Path:
    """
    Return path formatted as `<name>-sequence.txt`
    """
    return Path(f"{basename_pathname}-sequence.txt")


def format_tipping_points_path(basename_pathname: str) -> Path:
    """
    Return path formatted as `<name>-tipping_point.txt`
    """
    return Path(f"{basename_pathname}-tipping_point.txt")


def _strip_line(line: bytes) -> str:
    # Strip comments and surrounding white space
    return str(line).split("# ", 1)[0].strip()


def _parse_action(line: str, action_by_name: dict[str, Action]) -> tuple[Action, str]:
    # TODO Allow any number of actions to be combined(?)
    action_pattern = (
        rf"(?P<action_name>{action_name_pattern})"
        rf"(\(\s*(?P<action1_name>{action_name_pattern})\s*&\s*"
        rf"(?P<action2_name>{action_name_pattern})\s*\))?"
    )

    argb_hex_pattern = r"#[a-fA-F0-9]{8}"
    colour_pattern = rf"(?P<colour>{argb_hex_pattern})"

    pattern = rf"{action_pattern}(\s+{colour_pattern})?"

    match = re.fullmatch(pattern, line)

    if match is None:
        raise ValueError(f"Cannot parse action: {line}")

    action_name = match.group("action_name")
    action1_name = match.group("action1_name") or ""
    action2_name = match.group("action2_name") or ""
    colour = match.group("colour") or ""

    assert (action1_name == "" and action2_name == "") or (
        action1_name != "" and action2_name != ""
    )
    combine_actions = action1_name != ""

    if action_name in action_by_name:
        raise ValueError(
            f"Action {action_name} already defined: actions must be defined only once"
        )

    if not combine_actions:
        action = Action(action_name)
        action_by_name[action_name] = action
    else:
        if action1_name not in action_by_name:
            raise ValueError(
                f"Unknown action {action1_name}: actions to combine must be defined first"
            )

        if action2_name not in action_by_name:
            raise ValueError(
                f"Unknown action {action2_name}: actions to combine must be defined first"
            )

        action1 = action_by_name[action1_name]
        action2 = action_by_name[action2_name]

        action = ActionCombination(action_name, [action1, action2])
        action_by_name[action_name] = action

    action = action_by_name[action_name]

    return action, colour


def read_actions(
    actions_path: Path | io.IOBase,
) -> tuple[alias.Actions, alias.ColourByAction]:

    stream = open_stream(actions_path)
    actions: alias.Actions = []
    action_by_name: dict[str, Action] = {}
    colour_by_action: alias.ColourByAction = {}

    with stream:
        for line in stream:
            line_as_string = _strip_line(line)

            # Skip empty lines
            if len(line_as_string) > 0:
                action, colour = _parse_action(line_as_string, action_by_name)
                actions.append(action)

                if len(colour) > 0:
                    colour_by_action[action] = hex_to_rgba(colour)

    return actions, colour_by_action


# pylint: disable-next=too-many-locals
def _parse_sequence(
    line: str,
    action_by_name_and_edition: dict[tuple[str, int], Action],
) -> tuple[alias.Sequence, alias.TippingPoint]:

    def conditionally_add_node(
        name: str,
        edition: int,
        action_by_name_and_edition: dict[tuple[str, int], Action],
    ):
        if (name, edition) not in action_by_name_and_edition:
            action = Action(name, edition)
            action_by_name_and_edition[(name, edition)] = action

    from_action_pattern = (
        rf"(?P<from_action_name>{action_name_pattern})"
        rf"(\[(?P<from_edition>{edition_pattern})\])?"
    )
    to_action_pattern = (
        rf"(?P<to_action_name>{action_name_pattern})"
        rf"(\[(?P<to_edition>{edition_pattern})\])?"
    )
    tipping_point_pattern = r"(?P<tipping_point>\d+)"
    pattern = (
        rf"{from_action_pattern}\s+{to_action_pattern}(\s+{tipping_point_pattern})?"
    )

    match = re.fullmatch(pattern, line)

    if match is None:
        raise ValueError(f"Cannot parse sequence: {line}")

    from_action_name = match.group("from_action_name")
    from_edition = (
        int(match.group("from_edition"))
        if match.group("from_edition") is not None
        else 0
    )
    conditionally_add_node(from_action_name, from_edition, action_by_name_and_edition)

    to_action_name = match.group("to_action_name")
    to_edition = (
        int(match.group("to_edition")) if match.group("to_edition") is not None else 0
    )
    conditionally_add_node(to_action_name, to_edition, action_by_name_and_edition)

    tipping_point = (
        int(match.group("tipping_point"))
        if match.group("tipping_point") is not None
        else 0
    )

    from_action = action_by_name_and_edition[(from_action_name, from_edition)]
    to_action = action_by_name_and_edition[(to_action_name, to_edition)]

    return (from_action, to_action), tipping_point


def read_sequences(
    sequences_path: Path | io.IOBase,
) -> tuple[alias.Sequences, alias.TippingPointByAction]:
    """
    Read sequences of actions and an optional tipping point from a stream and return the
    information read

    :param sequences_path: Path of file to read from or an open stream to read from

    Comments are supported: everything after the first pound sign (#) on a line is
    skipped. Example::

        # Diverging sequences
        current a
        current b
        current c  # Third sequence
        # Done specifying sequences
    """
    stream = open_stream(sequences_path)
    sequences: alias.Sequences = []
    tipping_point_by_action: alias.TippingPointByAction = {}
    action_by_name_and_edition: dict[tuple[str, int], Action] = {}

    with stream:
        root_action_seen = False

        for line in stream:
            line_as_string = _strip_line(line)

            # Skip empty lines
            if len(line_as_string) > 0:
                sequence, tipping_point = _parse_sequence(
                    line_as_string,
                    action_by_name_and_edition,
                )
                if not root_action_seen and sequence[0].name == sequence[1].name:
                    root_action_seen = True
                else:
                    sequences.append(sequence)

                assert sequence[1] not in tipping_point_by_action, sequence[1]
                tipping_point_by_action[sequence[1]] = tipping_point

        if len(sequences) > 0 and not root_action_seen:
            raise ValueError(
                "Exactly one sequence must relate the root / current action with itself. "
                "This allows a tipping point to be defined for the graph's first action. "
                "Such a sequence is not present in the file. "
            )

    return sequences, tipping_point_by_action


# def _parse_tipping_point(
#     line: str,
#     action_by_name_and_edition: dict[tuple[str, int], Action],
# ) -> tuple[Action, int]:
#
#     action_pattern = (
#         rf"(?P<action_name>{action_name_pattern})"
#         rf"(\[(?P<edition>{edition_pattern})\])?"
#     )
#     tipping_point_pattern = r"(?P<tipping_point>\d+)"
#     pattern = rf"{action_pattern}\s+{tipping_point_pattern}"
#
#     match = re.fullmatch(pattern, line)
#
#     if match is None:
#         raise ValueError(f"Cannot parse tipping point: {line}")
#
#     action_name = match.group("action_name")
#     edition = int(match.group("edition")) if match.group("edition") is not None else 0
#     tipping_point = int(match.group("tipping_point"))
#
#     if not (action_name, edition) in action_by_name_and_edition:
#         raise ValueError(
#             f"Tipping point for unknown action {action_name} (edition {edition})"
#         )
#
#     action = action_by_name_and_edition[(action_name, edition)]
#
#     return action, tipping_point
#
#
# def read_tipping_points(
#     tipping_points_path: Path | io.IOBase,
#     action_by_name_and_edition: dict[tuple[str, int], Action],
# ) -> dict[Action, int]:
#
#     stream = open_stream(tipping_points_path)
#     tipping_point_by_action: dict[Action, int] = {}
#
#     with stream:
#         for line in stream:
#             line_as_string = _strip_line(line)
#
#             # Skip empty lines
#             if len(line_as_string) > 0:
#
#                 action, tipping_point = _parse_tipping_point(
#                     line_as_string,
#                     action_by_name_and_edition,
#                 )
#                 tipping_point_by_action[action] = tipping_point
#
#     return tipping_point_by_action


def read_dataset(
    basename_pathname: str,
) -> tuple[
    alias.Actions, alias.Sequences, alias.TippingPointByAction, alias.ColourByAction
]:
    """
    Read information about adaptation pathways from a set of text files

    The names of the text files read are fixed, see :py:func:`format_actions_path`,
    :py:func:`format_sequences_path`.

    Tipping points are optional. If they are not present, they will be initialized to zero.
    """
    actions_path = format_actions_path(basename_pathname)
    sequences_path = format_sequences_path(basename_pathname)

    actions, colour_by_action = read_actions(actions_path)
    sequences, tipping_point_by_action = read_sequences(sequences_path)

    action_names = [action.name for action in actions]

    for sequence in sequences:
        for action in sequence:
            if action.name not in action_names:
                raise ValueError(
                    f"Action {action.name} from {sequences_path} is not present in {actions_path}"
                )

    return actions, sequences, tipping_point_by_action, colour_by_action


def _format_action(action: Action | ActionCombination) -> str:
    result = f"{action.name}"

    if isinstance(action, ActionCombination):
        combined_actions = "&".join(
            combined_action.name for combined_action in action.actions
        )
        result += f"{action.name}({combined_actions})"

    return result


def write_actions(
    actions: alias.Actions, colour_by_action: alias.ColourByAction, path: Path
) -> None:
    with open(path, "w", encoding="utf8") as file:
        for action in actions:
            file.write(f"{_format_action(action)} {colour_by_action[action]}\n")


def write_sequences(sequences: alias.Sequences, path: Path) -> None:
    with open(path, "w", encoding="utf8") as file:
        for from_action, to_action in sequences:
            file.write(f"{_format_action(from_action)} {_format_action(to_action)}\n")


def write_tipping_points(
    tipping_points: alias.TippingPointByAction, path: Path
) -> None:
    with open(path, "w", encoding="utf8") as file:
        for action, tipping_point in tipping_points.items():
            file.write(f"{_format_action(action)} {tipping_point}\n")


def write_dataset(
    actions: alias.Actions,
    sequences: alias.Sequences,
    tipping_point_by_action: alias.TippingPointByAction,
    colour_by_action: alias.ColourByAction,
    basename_pathname: str,
) -> None:
    """
    Write the information about adaptation pathways to a set of text files

    The names of the created text files are fixed, see :py:func:`format_actions_path`,
    :py:func:`format_sequences_path`, :py:func:`format_tipping_points_path`. Existing files
    are overwritten.

    In case the tipping-point collection is empty, no tipping-point file is created.
    """
    actions_path = format_actions_path(basename_pathname)
    sequences_path = format_sequences_path(basename_pathname)
    tipping_points_path = format_tipping_points_path(basename_pathname)

    write_actions(actions, colour_by_action, actions_path)
    write_sequences(sequences, sequences_path)

    if len(tipping_point_by_action) > 0:
        write_tipping_points(tipping_point_by_action, tipping_points_path)
