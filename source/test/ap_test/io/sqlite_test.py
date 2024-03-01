import unittest

from adaptation_pathways.action import Action
from adaptation_pathways.io import sqlite as dbms


class SQLiteTest(unittest.TestCase):
    def test_write_read_roundtrip(self):
        database_path = "tesт_sævè_æß.db"
        current = Action("çürr€ñt")
        a = Action("æ")
        b = Action("ß")
        c = Action("ç")
        actions = [current, a, b, c]
        sequences = [
            (current, a),
            (a, b),
            (b, c),
        ]

        dbms.write_dataset(actions, sequences, database_path)

        actions_we_got, sequences_we_got = dbms.read_dataset(database_path)

        self.assertEqual(
            [action.name for action in actions_we_got],
            [action.name for action in actions],
        )

        self.assertEqual(
            sequences_we_got,
            [
                (
                    actions_we_got[
                        next(
                            idx
                            for idx, action in enumerate(actions_we_got)
                            if action.name == sequence[0].name
                        )
                    ],
                    actions_we_got[
                        next(
                            idx
                            for idx, action in enumerate(actions_we_got)
                            if action.name == sequence[1].name
                        )
                    ],
                )
                for sequence in sequences
            ],
        )

        self.assertRaises(
            RuntimeError,
            dbms.write_dataset,
            actions,
            sequences,
            database_path,
            overwrite=False,
        )
