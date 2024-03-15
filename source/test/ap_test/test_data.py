import copy
from io import StringIO

from adaptation_pathways.action import Action
from adaptation_pathways.action_combination import ActionCombination


def empty_stream():
    return StringIO(
        """
        """
    )


def serial_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")

    actions = [current, a, b, c]

    sequences = [
        (current, a),
        (a, b),
        (b, c),
    ]

    return actions, sequences


def diverging_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")

    actions = [current, a, b, c]

    sequences = [
        (current, a),
        (current, b),
        (current, c),
    ]

    return actions, sequences


def converging_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")

    actions = [current, a, b, c, d]

    sequences = [
        (current, a),
        (current, b),
        (current, c),
        (a, d),
        (b, d),
        (c, d),
    ]

    return actions, sequences


def action_combination_01_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    actions = [current, a, b, c]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    sequences = [
        (current, a),
        (current, b),
        (a, c1),
        (b, c2),
    ]

    return actions, sequences


def action_combination_02_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    # Combination before the actions combined
    actions = [current, c, a, b]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    sequences = [
        (current, a),
        (current, b),
        (a, c1),
        (b, c2),
    ]

    return actions, sequences


def action_combination_03_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = ActionCombination("c", [a, b])

    # Combination before the actions combined
    actions = [current, c, a, b]

    c1 = copy.copy(c)
    c2 = copy.copy(c)

    # Combination before the actions combined
    sequences = [
        (a, c1),
        (b, c2),
        (current, a),
        (current, b),
    ]

    return actions, sequences


def use_case_01_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")
    e = Action("e")
    f = Action("f")

    actions = [current, a, b, c, d, e, f]

    sequences = [
        (current, a),
        (a, e),
        (current, b),
        (b, f),
        (current, c),
        (c, f),
        (current, d),
        (d, f),
        (f, e),
    ]

    return actions, sequences


def use_case_02_pathway():
    current = Action("current")
    a = Action("a")
    b = Action("b")
    c = Action("c")
    d = Action("d")

    actions = [current, a, b, c, d]

    b1 = copy.copy(b)
    b2 = copy.copy(b)

    sequences = [
        (current, a),
        (current, b1),
        (current, c),
        (current, d),
        (b1, a),
        (b1, c),
        (b1, d),
        (c, b2),
        (b2, a),
        (c, a),
        (c, d),
    ]

    return actions, sequences
