import unittest

from adaptation_pathways.action import Action
from adaptation_pathways.io import sqlite as dbms
from adaptation_pathways.plot.colour import default_action_colours, rgba_to_hex

from .. import test_data


class SQLiteTest(unittest.TestCase):
    def compare_actions(self, actions_we_got, actions_we_want):
        # Compare the names of the actions
        self.assertEqual(
            [action.name for action in actions_we_got],
            [action.name for action in actions_we_want],
        )

        # Compare the types of the actions
        self.assertEqual(
            [type(action) for action in actions_we_got],
            [type(action) for action in actions_we_want],
        )

    def compare_sequences(self, sequences_we_got, sequences_we_want):
        # Compare the names of the actions in the sequences
        self.assertEqual(
            [(action1.name, action2.name) for action1, action2 in sequences_we_got],
            [(action1.name, action2.name) for action1, action2 in sequences_we_want],
        )

        # Compare the types of the actions in the sequences
        self.assertEqual(
            [(type(action1), type(action2)) for action1, action2 in sequences_we_got],
            [(type(action1), type(action2)) for action1, action2 in sequences_we_want],
        )

    def compare_colours(self, colours_we_got, colours_we_want):
        self.assertEqual(
            [(action.name, colour) for action, colour in colours_we_got.items()],
            [(action.name, colour) for action, colour in colours_we_want.items()],
        )

    def compare_data(  # pylint: disable=too-many-arguments
        self,
        actions,
        sequences,
        colours,
    ):
        self.compare_actions(*actions)
        self.compare_sequences(*sequences)
        self.compare_colours(*colours)

    def _test_round_trip(self, database_path, actions, sequences):
        colours = [
            rgba_to_hex(colour) for colour in default_action_colours(len(actions))
        ]
        colour_by_action = {action: colours[idx] for idx, action in enumerate(actions)}

        dbms.write_dataset(actions, sequences, colour_by_action, database_path)

        actions_we_got, sequences_we_got, colours_we_got = dbms.read_dataset(
            database_path
        )

        self.compare_data(
            (actions_we_got, actions),
            (sequences_we_got, sequences),
            (colours_we_got, colour_by_action),
        )

    def test_overwrite(self):
        database_path = "overwrite.db"
        actions = []
        sequences = []
        colours = {}

        dbms.write_dataset(actions, sequences, colours, database_path)
        self.assertRaises(
            RuntimeError,
            dbms.write_dataset,
            actions,
            sequences,
            colours,
            database_path,
            overwrite=False,
        )

    def test_encoding(self):
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
        self._test_round_trip(database_path, actions, sequences)

    def test_serial_pathway(self):
        database_path = "test_serial_pathway.db"
        actions, sequences = test_data.serial_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_diverging_pathway(self):
        database_path = "test_diverging_pathway.db"
        actions, sequences = test_data.diverging_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_converging_pathway(self):
        database_path = "test_converging_pathway.db"
        actions, sequences = test_data.converging_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_action_combination_01_pathway(self):
        database_path = "test_action_combination_01_pathway.db"
        actions, sequences = test_data.action_combination_01_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_action_combination_02_pathway(self):
        database_path = "test_action_combination_02_pathway.db"
        actions, sequences = test_data.action_combination_02_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_action_combination_03_pathway(self):
        database_path = "test_action_combination_03_pathway.db"
        actions, sequences = test_data.action_combination_03_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_use_case_01_pathway(self):
        database_path = "test_use_case_01_pathway.db"
        actions, sequences = test_data.use_case_01_pathway()
        self._test_round_trip(database_path, actions, sequences)

    def test_use_case_02_pathway(self):
        database_path = "test_use_case_02_pathway.db"
        actions, sequences = test_data.use_case_02_pathway()
        self._test_round_trip(database_path, actions, sequences)
