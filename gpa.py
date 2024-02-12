import re

import pandas as pd


class MyValueError(Exception):
    def __init__(self, line):
        self.line = line

    pass


def text2df(txt_grade):

    main_text = txt_grade.split("年度	期間")[-1]
    main_text = main_text.split("修得単位状況")[0]
    lines = main_text.split("\n")

    main_category = ""
    sub_category = ""

    grade_list = []
    for line in lines:
        # cols = re.split("[ \t]+", line)
        cols = line.split("\t")
        if len(cols) == 1:
            if cols[0] == "":
                continue  # skip
            elif cols[0][0] == " ":
                sub_category = cols[0].replace(" ", "")
            else:
                main_category = cols[0]
            continue
        cols = [col.replace(" ", "") for col in cols]
        if (
            len(cols) == 9
        ):  # ['教科名', 'メディア授業科目', '担当教員', '選択／必修?', '単位', '得点', '評価', '年度', '期間']
            cols[-2] = int(cols[-2])  # 年度
            cols[-5] = 0.0 if cols[-5] == "" else float(cols[-5])  # 単位数
            try:
                grade_as_gpa = float(cols[-3])
                grade_as_gpa = grade_num2gpa(grade_as_gpa)
            except:
                grade_as_gpa = grade_alp2gpa(cols[-3])
            cols.insert(-2, grade_as_gpa)  # GPA換算成績
            grade_list.append([main_category, sub_category, *cols])
        else:
            raise MyValueError(line)
    df_grade = pd.DataFrame(
        grade_list,
        columns=[
            "科目分類(大)",
            "科目分類(小)",
            "科目名",
            "メディア授業科目",
            "担当教員",
            "選択／必修",
            "単位",
            "得点",
            "評価",
            "GPA換算成績",
            "年度",
            "期間",
        ],
    )
    return df_grade


def grade_alp2gpa(grade):
    if grade == "ＡＡ":
        return 4.0
    elif grade == "Ａ":
        return 3.0
    elif grade == "Ｂ":
        return 2.0
    elif grade == "Ｃ":
        return 1.0
    else:
        return 0.0


def grade_num2gpa(grade):
    if grade >= 90.0:
        return 4.0
    elif grade >= 80.0:
        return 3.0
    elif grade >= 70.0:
        return 2.0
    elif grade >= 60.0:
        return 1.0
    else:
        return 0.0


if __name__ == "__main__":
    file_name = "grade_phone.txt"
    file_name = "grade_pc.txt"
    with open(file_name, "r", encoding="utf-8") as f:
        txt_grade = f.read()

    main_text = txt_grade.split("年度	期間")[-1]
    main_text = main_text.split("修得単位状況")[0]
    df_grade = text2df(txt_grade)

    sum_credits = df_grade["単位"].sum()
    gpa = (df_grade["GPA換算成績"] * df_grade["単位"]).sum() / sum_credits
    print("GPA: {:.2f}".format(gpa))
    print("総取得単位数: {}".format(sum_credits))
