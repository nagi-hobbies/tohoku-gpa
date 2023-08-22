import re

import pandas as pd


class MyValueError(Exception):
    def __init__(self, line):
        self.line = line

    pass


def parse_grade(grade_text):
    grade_list = []
    main_category = ""
    sub_category = ""
    lines = grade_text.split("\n")
    for line in lines:
        cols = re.split("[ \t]+", line)
        if len(cols) == 1:
            main_category = cols[0]
        elif len(cols) == 2:
            sub_category = cols[1]
        elif len(cols) == 8:
            cols[-2] = int(cols[-2])
            cols[-4] = float(cols[-4])
            grade_list.append([main_category, sub_category, *cols[1:]])
        elif len(cols) == 6:
            pass
        else:
            raise MyValueError(line)
    grade_data = pd.DataFrame(
        grade_list,
        columns=[
            "科目分類(大)",
            "科目分類(小)",
            "教科名",
            "教授名",
            "選択or必修or?",
            "単位数",
            "成績",
            "取得年度",
            "前期or後期",
        ],
    )
    return grade_data


def get_gpa(ug_arr):
    """
    ug_arr: 2次元配列，単位数と成績の配列
    """
    gpa = 0
    total_credits = 0
    for ug in ug_arr:
        crdt = ug[0]
        grade = ug[1]
        if grade == "ＡＡ":
            gpa += 4 * crdt
        elif grade == "Ａ":
            gpa += 3 * crdt
        elif grade == "Ｂ":
            gpa += 2 * crdt
        elif grade == "Ｃ":
            gpa += 1 * crdt
        else:
            continue
        total_credits += crdt
    gpa = gpa / total_credits
    return gpa, total_credits
