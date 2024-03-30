from .. import alias
from . import sqlite, text


def read_dataset(
    basename_pathname: str,
) -> tuple[
    alias.Actions, alias.Sequences, alias.TippingPointByAction, alias.ColourByAction
]:
    sqlite_dataset_exists = sqlite.dataset_exists(basename_pathname)

    try:
        if sqlite.dataset_exists(basename_pathname):
            # pylint: disable-next=unused-variable
            actions, sequences, tipping_point_by_action, colour_by_action = (
                sqlite.read_dataset(basename_pathname)
            )
        else:
            # pylint: disable-next=unused-variable
            actions, sequences, tipping_point_by_action, colour_by_action = (
                text.read_dataset(basename_pathname)
            )
    except Exception as exception:
        if sqlite_dataset_exists:
            message = f"Error while reading binary dataset {basename_pathname}"
        else:
            message = (
                f"Error while reading text dataset {basename_pathname}. "
                "First tried reading a binary dataset with that name "
                "but it does not exist."
            )
        raise RuntimeError(message) from exception

    return actions, sequences, tipping_point_by_action, colour_by_action
