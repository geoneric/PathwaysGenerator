import sqlite3
from pathlib import Path

from ..action import Action


_action_table_name = "action"
_sequence_table_name = "sequence"
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


def write_dataset(
    actions: list[Action],
    sequences: list[tuple[Action, Action]],
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
            id INTEGER NOT NULL,
            name TEXT NOT NULL UNIQUE,

            PRIMARY KEY (id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_sequence_table_name}
        (
            id INTEGER NOT NULL,
            from_action_id INTEGER NOT NULL,
            to_action_id INTEGER NOT NULL,

            PRIMARY KEY (id),
            FOREIGN KEY (from_action_id) REFERENCES {_action_table_name} (id),
            FOREIGN KEY (to_action_id) REFERENCES {_action_table_name} (id)
        )
        """
    )
    connection.execute(
        f"""
        CREATE TABLE {_plot_table_name}
        (
            id INTEGER NOT NULL,
            rgba TEXT NOT NULL,
            action_id INTEGER NOT NULL,

            PRIMARY KEY (id),
            FOREIGN KEY (action_id) REFERENCES {_action_table_name} (id)
        )
        """
    )

    action_records = (
        {"id": idx, "name": action.name} for idx, action in enumerate(actions)
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_action_table_name}
            (
                id,
                name
            )
            VALUES
            (
                :id,
                :name
            )
            """,
            action_records,
        )

    sequence_records = (
        {
            "id": idx,
            "from_action_id": actions.index(sequence[0]),
            "to_action_id": actions.index(sequence[1]),
        }
        for idx, sequence in enumerate(sequences)
    )

    with connection:
        connection.executemany(
            f"""
            INSERT INTO {_sequence_table_name}
            (
                id,
                from_action_id,
                to_action_id
            )
            VALUES
            (
                :id,
                :from_action_id,
                :to_action_id
            )
            """,
            sequence_records,
        )

    connection.close()


def read_dataset(
    database_path: Path | str,
) -> tuple[list[Action], list[tuple[Action, Action]]]:
    """
    Open the database and return the contents

    :return: Tuple of actions and sequences read
    """
    database_path = normalize_database_path(database_path)

    connection = sqlite3.connect(f"file:{database_path}?mode=ro", uri=True)
    action_data = list(connection.execute(f"SELECT id, name from {_action_table_name}"))
    actions = [Action(record[1]) for record in action_data]

    sequence_data = connection.execute(
        f"SELECT id, from_action_id, to_action_id from {_sequence_table_name}"
    )
    sequences = [
        (
            actions[
                next(
                    idx
                    for idx, action_record in enumerate(action_data)
                    if sequence_record[1] == action_record[0]
                )
            ],
            actions[
                next(
                    idx
                    for idx, action_record in enumerate(action_data)
                    if sequence_record[2] == action_record[0]
                )
            ],
        )
        for sequence_record in sequence_data
    ]

    connection.close()

    return actions, sequences
