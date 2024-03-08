import copy
import sqlite3
from pathlib import Path

from ..action import Action
from ..action_combination import ActionCombination


_action_table_name = "action"
_edition_table_name = "edition"
_sequence_table_name = "sequence"
_action_combination_table_name = "action_combination"
_plot_table_name = "plot"
_default_database_path_suffix = ".apw"


def normalize_database_path(database_path: Path | str) -> Path:
    """
    Perform a number of updates to the path passed in

    - If the type is string, convert it to a Path
    - If the path does not have a suffix, add the default one
    """
    if isinstance(database_path, str):
        database_path = Path(database_path)

    # Only add the default suffix if the path doesn't already have one
    if len(database_path.suffix) == 0:
        database_path = database_path.with_suffix(_default_database_path_suffix)

    return database_path


def write_dataset(  # pylint: disable=too-many-locals
    actions: list[Action],
    sequences: list[tuple[Action, Action]],
    colours: dict[Action, str],
    database_path: Path | str,
    *,
    overwrite: bool = True,
) -> None:
    """
    Save the information passed in to the database
    """
    database_path = normalize_database_path(database_path)

    if database_path.exists() and not overwrite:
        raise RuntimeError(f"Database {database_path} already exists")

    database_path.unlink(missing_ok=True)

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = 1")

    connection.execute(
        f"""
        CREATE TABLE {_action_table_name}
        (
            action_id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,

            PRIMARY KEY (action_id)
        )
        """
    )

    # edition_id is just a unique number identifying a unique action + edition combination
    connection.execute(
        f"""
        CREATE TABLE {_edition_table_name}
        (
            action_id INTEGER NOT NULL,
            edition_id INTEGER NOT NULL,

            FOREIGN KEY (action_id) REFERENCES {_action_table_name} (action_id),
            PRIMARY KEY (edition_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_sequence_table_name}
        (
            sequence_id INTEGER NOT NULL,
            from_edition_id INTEGER NOT NULL,
            to_edition_id INTEGER NOT NULL,

            PRIMARY KEY (sequence_id),
            FOREIGN KEY (from_edition_id)
                REFERENCES {_edition_table_name} (edition_id),
            FOREIGN KEY (to_edition_id)
                REFERENCES {_edition_table_name} (edition_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_action_combination_table_name}
        (
            edition_id INTEGER NOT NULL,
            combined_edition_id INTEGER NOT NULL,

            UNIQUE (edition_id, combined_edition_id),
            FOREIGN KEY (edition_id)
                REFERENCES {_edition_table_name} (edition_id),
            FOREIGN KEY (combined_edition_id)
                REFERENCES {_edition_table_name} (edition_id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_plot_table_name}
        (
            action_id INTEGER NOT NULL,
            colour TEXT NOT NULL,

            PRIMARY KEY (action_id),
            FOREIGN KEY (action_id) REFERENCES {_action_table_name} (action_id)
        )
        """
    )

    action_id_by_name = {
        action.name: action_id for action_id, action in enumerate(actions)
    }
    action_records = (
        {"action_id": action_id_by_name[action.name], "name": action.name}
        for action in actions
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_action_table_name}
            (
                action_id,
                name
            )
            VALUES
            (
                :action_id,
                :name
            )
            """,
            action_records,
        )

    # Sequences contain actions. Actions have a unique name. Actions with the same name are
    # the same action: they must have the same action_id. In the sequences, these actions must
    # be the same instance (have the same id()).
    # Actions with the same name, but with different id()'s are different instances of the
    # same action. They must be treated as being different editions. Actions with different
    # editions can be associated with different tipping points.

    # All unique Action instances, by name
    action_instances_by_name: dict[str, list[Action]] = {}

    # All unique Action instances, is some order
    action_instances: list[Action] = []

    def add_action_instance(action):
        if action.name not in action_instances_by_name:
            action_instances_by_name[action.name] = [action]
            action_instances.append(action)
        elif action not in action_instances_by_name[action.name]:
            action_instances_by_name[action.name].append(action)
            action_instances.append(action)

    for sequence in sequences:
        for action in sequence:
            if isinstance(action, ActionCombination):
                for combined_action in action.actions:
                    add_action_instance(combined_action)

            add_action_instance(action)

    # Action edition ID by instance, in some order
    edition_id_by_instance = {
        action: edition_id for edition_id, action in enumerate(action_instances)
    }

    edition_records = (
        {
            "action_id": action_id_by_name[action.name],
            "edition_id": edition_id,
        }
        for action, edition_id in edition_id_by_instance.items()
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_edition_table_name}
            (
                action_id,
                edition_id
            )
            VALUES
            (
                :action_id,
                :edition_id
            )
            """,
            edition_records,
        )

    sequence_records = (
        {
            "sequence_id": sequence_id,
            "from_edition_id": edition_id_by_instance[sequence[0]],
            "to_edition_id": edition_id_by_instance[sequence[1]],
        }
        for sequence_id, sequence in enumerate(sequences)
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_sequence_table_name}
            (
                sequence_id,
                from_edition_id,
                to_edition_id
            )
            VALUES
            (
                :sequence_id,
                :from_edition_id,
                :to_edition_id
            )
            """,
            sequence_records,
        )

    # Action combination are actions that combine other actions. In the table we relate the id
    # of the action combination with the id's of the actions that are combined. In principle
    # any number (≥ 2) of actions can be combined into a single action combination.
    action_combination_records = []

    for action, edition_id in edition_id_by_instance.items():
        if isinstance(action, ActionCombination):
            for combined_action in action.actions:
                action_combination_records.append(
                    {
                        "edition_id": edition_id,
                        "combined_edition_id": edition_id_by_instance[combined_action],
                    }
                )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_action_combination_table_name}
            (
                edition_id,
                combined_edition_id
            )
            VALUES
            (
                :edition_id,
                :combined_edition_id
            )
            """,
            action_combination_records,
        )

    plot_records = (
        {"action_id": action_id_by_name[action.name], "colour": colours[action]}
        for action in actions
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_plot_table_name}
            (
                action_id,
                colour
            )
            VALUES
            (
                :action_id,
                :colour
            )
            """,
            plot_records,
        )

    connection.close()


def read_dataset(  # pylint: disable=too-many-locals
    database_path: Path | str,
) -> tuple[list[Action], list[tuple[Action, Action]], dict[Action, str]]:
    """
    Open the database and return the contents

    :return: Tuple of actions and sequences read
    """
    database_path = normalize_database_path(database_path)

    connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
    connection.execute("PRAGMA foreign_keys = 1")

    # TODO Use SQL for this?! We've got all relations set up. Use'm!

    action_combination_data = list(
        connection.execute(
            f"""
            SELECT edition_id, combined_edition_id
            FROM {_action_combination_table_name}
            """
        )
    )
    combined_edition_ids_by_edition_id: dict[int, list[int]] = {}

    for edition_id, combined_edition_id in action_combination_data:
        combined_edition_ids_by_edition_id.setdefault(edition_id, []).append(
            combined_edition_id
        )

    edition_data = list(
        connection.execute(f"SELECT action_id, edition_id from {_edition_table_name}")
    )

    action_id_by_edition_id: dict[int, int] = {
        edition_id: action_id for action_id, edition_id in edition_data
    }

    combined_action_ids_by_action_id: dict[int, list[int]] = {
        action_id_by_edition_id[edition_id]: [
            action_id_by_edition_id[edition_id] for edition_id in combined_edition_ids
        ]
        for edition_id, combined_edition_ids in combined_edition_ids_by_edition_id.items()
    }

    action_data = list(
        connection.execute(f"SELECT action_id, name from {_action_table_name}")
    )
    action_instance_by_id: dict[int, Action | ActionCombination] = {}

    for action_id, name in action_data:
        if action_id not in combined_action_ids_by_action_id:
            action_instance_by_id[action_id] = Action(name)
        else:
            # Placeholder. First add the regular actions. The ones to combine may come after the
            # current combination.
            action_instance_by_id[action_id] = Action(name)

    for action_id, name in action_data:
        if action_id in combined_action_ids_by_action_id:
            combined_action_ids = combined_action_ids_by_action_id[action_id]
            combined_actions = [
                action_instance_by_id[combined_action_id]
                for combined_action_id in combined_action_ids
            ]
            action_instance_by_id[action_id] = ActionCombination(name, combined_actions)

    actions: list[Action | ActionCombination] = [
        action_instance_by_id[record[0]] for record in action_data
    ]

    action_instance_by_edition: dict[tuple[str, int], Action] = {
        edition_id: copy.copy(action_instance_by_id[action_id])
        for action_id, edition_id in edition_data
    }

    sequence_data = connection.execute(
        f"SELECT sequence_id, from_edition_id, to_edition_id from {_sequence_table_name}"
    )

    sequences = [
        (
            action_instance_by_edition[sequence_record[1]],
            action_instance_by_edition[sequence_record[2]],
        )
        for sequence_record in sequence_data
    ]

    plot_data = connection.execute(f"SELECT action_id, colour from {_plot_table_name}")

    colours = {
        action_instance_by_id[plot_record[0]]: plot_record[1]
        for plot_record in plot_data
    }

    connection.close()

    return actions, sequences, colours
