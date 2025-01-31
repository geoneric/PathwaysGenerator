import flet as ft


class FloatInputFilter(ft.InputFilter):
    def __init__(self):
        super().__init__(
            regex_string=r"^$|^[-+]?\d*(\.\d*)?$", allow=True, replacement_string=""
        )


class IntInputFilter(ft.InputFilter):
    def __init__(self):
        super().__init__(regex_string=r"^-?\d*$", allow=True, replacement_string="")
