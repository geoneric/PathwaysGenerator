# pylint: disable=too-many-arguments
from typing import Callable

import flet as ft

from .. import theme
from .sortable_header import SortableHeader, SortMode
from .styled_button import StyledButton


class TableColumn:
    def __init__(
        self,
        label: str,
        key: str | None = None,
        expand: bool | int | None = True,
        sortable: bool = True,
        width: int | None = None,
        alignment: ft.Alignment | None = ft.alignment.center_left,
    ):
        self.label = label
        self.expand = expand
        self.key = label if key is None else key
        self.alignment = alignment
        self.width = width
        self.sortable = sortable


class TableCell:
    def __init__(
        self,
        control: ft.Control,
        sort_value: int | float | str | None = None,
    ):
        self.control = control
        self.sort_value = sort_value
        self.on_sort_value_changed: Callable[[], None] | None = None

    def set_sort_value(self, value: int | float | str | None):
        self.sort_value = value
        if self.on_sort_value_changed is not None:
            self.on_sort_value_changed()


class TableRow:
    def __init__(self, row_id: str, cells: list[TableCell], can_be_deleted=True):
        self.row_id = row_id
        self.cells = cells
        self.can_be_deleted = can_be_deleted


class ColumnData:
    def __init__(
        self,
        column: TableColumn,
        height: int,
        on_sort: Callable[[SortableHeader], None] | None = None,
    ):
        self.column = column
        self.header = SortableHeader(
            name=column.label,
            sort_key=column.key,
            sort_mode=(SortMode.UNSORTED if column.sortable else SortMode.NONE),
            on_sort=on_sort,
            expand=column.expand,
            bgcolor=theme.colors.primary_lightest,
            width=column.width,
            height=height,
        )


class RowData:
    def __init__(
        self,
        row: TableRow,
        initial_index: int,
        columns: list[ColumnData],
        height: int,
        on_selected: Callable[["RowData"], None] | None = None,
    ):
        self.row = row
        self.initial_index = initial_index
        self.on_selected = on_selected
        self.checkbox = ft.Checkbox(
            value=False,
            on_change=self.on_checkbox_clicked,
        )
        self.height = height
        self.control = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        content=self.checkbox,
                        padding=theme.variables.table_cell_padding,
                        width=40,
                        height=height,
                    ),
                    *(
                        self._create_cell_control(cell, index, columns)
                        for index, cell in enumerate(self.row.cells)
                    ),
                ],
                spacing=0,
            ),
            expand=True,
        )

    def on_checkbox_clicked(self, _):
        if self.on_selected is None:
            return
        self.on_selected(self)

    def _create_cell_control(
        self, cell: TableCell, index: int, columns: list[ColumnData]
    ):
        column = columns[index].column
        return ft.Container(
            content=cell.control,
            expand=column.expand,
            height=self.height,
            width=column.width,
            padding=None,
        )


class StyledTable(ft.Container):
    def __init__(
        self,
        columns: list[TableColumn],
        rows: list[TableRow],
        row_height=36,
        sort_column_index: int | None = None,
        sort_ascending: bool = True,
        on_sorted: Callable[[], None] | None = None,
        on_add: Callable[[], None] | None = None,
        add_label="Add",
        on_delete: Callable[[list[TableRow]], None] | None = None,
        delete_label="Delete",
        on_copy: Callable[[list[TableRow]], None] | None = None,
        copy_label="Duplicate",
        pre_operation_content: ft.Control | None = None,
        show_checkboxes=False,
        expand: bool | int | None = True,
    ):
        super().__init__(
            expand=expand,
        )

        self.row_height = row_height
        self.sort_column_index = sort_column_index
        self.sort_ascending = sort_ascending
        self.show_checkboxes = show_checkboxes
        self.on_sorted = on_sorted

        self.on_add = on_add
        self.on_copy = on_copy
        self.on_delete = on_delete

        self.selected_row_ids: set[str] = set()
        self.add_button = StyledButton(
            add_label, ft.Icons.ADD_CIRCLE_OUTLINE, on_click=self.on_add_clicked
        )
        self.copy_button = StyledButton(
            copy_label, ft.Icons.ADD_CIRCLE_OUTLINE, on_click=self.on_copy_clicked
        )
        self.delete_button = StyledButton(
            delete_label,
            ft.Icons.REMOVE_CIRCLE_OUTLINE,
            on_click=self.on_delete_clicked,
        )
        self.operation_row = ft.Row(
            [self.delete_button, self.copy_button, self.add_button],
            expand=True,
            alignment=ft.MainAxisAlignment.END,
        )
        if pre_operation_content is not None:
            self.operation_row.controls.insert(0, pre_operation_content)

        self.operations = ft.Container(self.operation_row, height=36)
        self.column_data: list[ColumnData] = []

        self.header_row = ft.Container(
            content=ft.Row([], expand=False, spacing=0),
            bgcolor=theme.colors.primary_lightest,
            border=ft.border.only(
                bottom=ft.BorderSide(1, theme.colors.primary_medium),
            ),
        )

        self.row_data: list[RowData] = []
        self.row_container = ft.Container(
            content=ft.Column([], expand=True, scroll=ft.ScrollMode.ALWAYS, spacing=0),
            expand=True,
        )

        self.content = ft.Column(
            [self.operations, self.header_row, self.row_container],
            spacing=0,
            expand=True,
        )

        self.set_columns(columns)
        self.set_rows(rows)

    def set_columns(self, columns: list[TableColumn]):
        self.column_data = [
            ColumnData(
                column=column, height=self.row_height, on_sort=self.on_header_sorted
            )
            for column in columns
        ]
        self.select_all_checkbox = ft.Checkbox(
            on_change=self.on_all_rows_selected,
        )
        self.header_row.content.controls = [
            ft.Container(
                content=self.select_all_checkbox,
                width=40,
                height=self.row_height,
                bgcolor=theme.colors.primary_lightest,
                padding=theme.variables.table_cell_padding,
            ),
            *(column.header for column in self.column_data),
        ]

    def set_rows(self, rows: list[TableRow]):
        self.row_data = [
            RowData(
                row=row,
                initial_index=index,
                columns=self.column_data,
                height=self.row_height,
                on_selected=self.on_row_selected,
            )
            for index, row in enumerate(rows)
        ]

        for row in self.row_data:
            for cell in row.row.cells:
                cell.on_sort_value_changed = self.sort_rows

        self.sort_rows()
        self.update_selected_rows()

    def sort_rows(self):
        self.row_data.sort(key=self.get_sort_value, reverse=not self.sort_ascending)
        self.row_container.content.controls = [row.control for row in self.row_data]
        self.update_selected_rows()

    def get_sort_value(self, row: RowData):
        if self.sort_column_index is None:
            return row.initial_index

        cell = row.row.cells[self.sort_column_index]
        return cell.sort_value

    def on_header_sorted(self, header: SortableHeader):
        column_index = None
        for index, column in enumerate(self.column_data):
            if column.header == header:
                column_index = index

        self.sort_ascending = header.sort_mode != SortMode.DESCENDING
        self.sort_column_index = (
            None if header.sort_mode == SortMode.UNSORTED else column_index
        )

        for index, column in enumerate(self.column_data):
            if index != self.sort_column_index:
                column.header.set_sort_mode(
                    SortMode.NONE
                    if column.header.sort_mode is SortMode.NONE
                    else SortMode.UNSORTED
                )

        self.sort_rows()
        self.update()

        if self.on_sorted is not None:
            self.on_sorted()

    def on_row_selected(self, row: RowData):
        if row.row.row_id in self.selected_row_ids:
            self.selected_row_ids.remove(row.row.row_id)
        else:
            self.selected_row_ids.add(row.row.row_id)
        self.update_selected_rows()
        self.update()

    def on_all_rows_selected(self, _):
        if self.select_all_checkbox.value:
            for row in self.row_data:
                self.selected_row_ids.add(row.row.row_id)
        else:
            self.selected_row_ids.clear()

        self.update_selected_rows()
        self.update()

    def update_selected_rows(self):
        self.copy_button.visible = (
            len(self.selected_row_ids) > 0 and self.on_copy is not None
        )
        self.add_button.visible = (
            not self.copy_button.visible and self.on_add is not None
        )

        deletable_count = sum(
            data.row.can_be_deleted and data.row.row_id in self.selected_row_ids
            for data in self.row_data
        )
        self.delete_button.visible = deletable_count > 0 and self.on_delete is not None

        self.select_all_checkbox.value = len(self.selected_row_ids) >= len(
            self.row_data
        )

        for index, row in enumerate(self.row_data):
            is_selected = row.row.row_id in self.selected_row_ids
            row.control.bgcolor = (
                theme.colors.row_selected
                if is_selected
                else (
                    theme.colors.true_white
                    if index % 2 == 0
                    else theme.colors.off_white
                )
            )
            row.checkbox.value = is_selected

    def on_add_clicked(self, _):
        if self.on_add is None:
            return

        self.on_add()

    def on_copy_clicked(self, _):
        if self.on_copy is None:
            return

        rows_to_copy = [
            data.row
            for data in self.row_data
            if data.row.row_id in self.selected_row_ids
        ]
        self.selected_row_ids.clear()
        self.on_copy(rows_to_copy)

    def on_delete_clicked(self, _):
        if self.on_delete is None:
            return

        rows_to_delete = [
            data.row
            for data in self.row_data
            if data.row.can_be_deleted and data.row.row_id in self.selected_row_ids
        ]
        self.selected_row_ids.clear()
        self.on_delete(rows_to_delete)
