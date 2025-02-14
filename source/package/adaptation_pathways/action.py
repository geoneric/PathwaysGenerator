"""
An action is a synonym for policy action, intervention, and measure, for example.
"""


class Action:
    """
    Actions are simply represented by a name

    :param name: Name of the action. It is required that different actions have different names.

    Some information is unique for an action, like its name. Other possible attributes depend on the
    application, but likely include a colour for plotting actions, a description, to provide help in a UI, and
    a vertical level for ordering actions in a metro map. Information that is unique for an action can be
    related to action names. All Action instances can lookup this information by action name.

    Other information must be related to the action instance, not its name. For example, a tipping point is
    always related to an Action instance. The same action, with the same name can occur multiple times in a
    set of pathways, and each instance has to be related to a likely different tipping point.
    """

    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return f'Action("{self._name}")'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
