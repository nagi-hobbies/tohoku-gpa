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
        cols = re.split("[ \t]+", line)
        if len(cols) == 1:  # [''] or ['main_category']
            if cols[0] == "":
                continue
            main_category = cols[0]
        elif len(cols) == 2:  # ['', 'sub_category']
            sub_category = cols[1]
        elif (
            len(cols) == 8
        ):  # ['', '教科名', '教授名', '選択or必修or?', '単位数', '成績', '取得年度', '前期or後期']
            cols[-2] = int(cols[-2])  # 取得年度
            cols[-4] = float(cols[-4])  # 単位数
            cols.insert(-2, grade2gpa(cols[-3]))
            grade_list.append([main_category, sub_category, *cols[1:]])
        elif (
            len(cols) == 6
        ):  # ['', '教科名', '教授名', '選択or必修or?', '取得年度', '前期or後期']
            cols[-2] = int(cols[-2])  # 取得年度
            cols.insert(-2, "")  # 成績
            cols.insert(-3, 0.)  # 単位数
            cols.insert(-2, 0)  # GPA
            grade_list.append([main_category, sub_category, *cols[1:]])
        else:
            raise MyValueError(line)
    df_grade = pd.DataFrame(
        grade_list,
        columns=[
            "科目分類(大)",
            "科目分類(小)",
            "科目名",
            "担当教員",
            "選択／必修",
            "単位",
            "評価",
            "GPA換算成績",
            "年度",
            "期間",
        ],
    )
    return df_grade

def grade2gpa(grade):
    if grade == "ＡＡ":
        return 4
    elif grade == "Ａ":
        return 3
    elif grade == "Ｂ":
        return 2
    elif grade == "Ｃ":
        return 1
    else:
        return 0


if __name__ == "__main__":
    file_name = "grade_phone.txt"
    file_name = "grade_pc.txt"
    with open(file_name, "r", encoding="utf-8") as f:
        txt_grade = f.read()
    text2df(txt_grade)

    df_grade = text2df(txt_grade)

    sum_credits = df_grade["単位"].sum()
    gpa = (df_grade["GPA換算成績"] * df_grade["単位"]).sum() / sum_credits
    print("GPA: {:.2f}".format(gpa))
    print("総取得単位数: {}".format(sum_credits))

