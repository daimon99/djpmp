# coding: utf-8
import copy
import datetime
import decimal
from typing import List

import xlwt

# Percent style
style_percent = xlwt.easyxf(num_format_str=r"0.00%")
style_border = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;')


def write_row(sheet, row_index, cols: List):
    """
    Write row in excel sheet.

    :param sheet: active sheet
    :param row_index: which row
    :param cols: values. If tuple, then the 1st is the value, and the 2nd is the style; If value, then the style is auto.

    :return: None
    """
    for col_index, val in enumerate(cols):
        if isinstance(val, tuple) or isinstance(val, list):
            value = val[0]
            style = val[1]
        else:
            value = val
            style = xlwt.Style.default_style
        sheet.write(row_index, col_index, value, style)


class SheetTpl:
    def __init__(self, sheet: xlwt.Worksheet):
        self.sheet = sheet
        self.basic_style = """
borders: left thin, right thin, top thin, bottom thin;
pattern: pattern solid;
alignment: wrap true;
"""
        self.current_style = None
        self.reset_style()

    def reset_style(self):
        self.current_style = xlwt.easyxf(self.basic_style)

    def write_row(self, row_index, cols: List):
        """
        Write row in excel sheet.

    :param sheet: active sheet
    :param row_index: which row
    :param cols: values. If tuple, then the 1st is the value, and the 2nd is the style; If value, then the style is auto.

    :return: None
        """
        for col_index, val in enumerate(cols):
            if isinstance(val, tuple) or isinstance(val, list):
                value = val[0]
                style = val[1]
            else:
                value = val
                style = self.current_style
                if isinstance(value, decimal.Deciaml):
                    style = self.style_money_format
                elif isinstance(value, datetime.date):
                    style = self.style_date_format
            self.sheet.write(row_index, col_index, value, style)

    def write_merge(self, r1, r2, c1, c2, value, style=None):
        style = style if style else self.current_style
        self.sheet.write_merge(r1, r2, c1, c2, value, style)

    def write(self, row, col, value, style=None):
        style = style if style else self.current_style
        self.sheet.write(row, col, value, style)

    def set_title(self):
        style: xlwt.XFStyle = self.current_style
        style.alignment.horz = style.alignment.HORZ_CENTER
        style.font.bold = True
        return style

    @property
    def style_percent_format(self):
        style = self.copy_style()
        style.num_format_str = r"0.00%"
        return style

    @property
    def style_date_format(self):
        style = self.copy_style()
        style.num_format_str = 'YYYY-M-D'
        return style

    @property
    def style_money_format(self):
        style = self.copy_style()
        style.num_format_str = '￥#,##0.00'
        return style

    def copy_style(self) -> xlwt.XFStyle:
        return copy.deepcopy(self.current_style)

    def set_cols_width(self, col_width_list: list):
        for i, col_width in enumerate(col_width_list):
            self.sheet.col(i).width = 256 * col_width * 2
