import pandas as pd


class GpaCalculator:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        bodies = self.raw_text.split("\n\n")
        # 一番長いテキストを選択
        self.raw_text = max(bodies, key=len)
        self.grades = self.parse_grades()

    def parse_grades(self):
        # Parse the raw text to extract grades and credits
        data = []
        lines = self.raw_text.splitlines()
        for line in lines:
            if "\t" in line and not "教員氏名" in line and not "合計単位" in line:
                parts = line.split("\t")
                if len(parts) >= 4:
                    try:
                        try:
                            credit = float(parts[1])
                        except ValueError:
                            credit = ""
                        grade = parts[2]
                        gpa_target = parts[3]
                        data.append(
                            (
                                parts[0],
                                credit,
                                grade,
                                gpa_target,
                                parts[4],
                                parts[5],
                                parts[6],
                            )
                        )
                    except:
                        print(parts)
                        raise ValueError("成績の形式がおかしいようです")
        if not data:
            raise ValueError("未知のデータ形式です。")
        df = pd.DataFrame(
            data,
            columns=["科目", "単位数", "評価", "GPA対象", "年度", "学期", "教員氏名"],
        )
        return df

    def grade_to_gpa(self, grade):
        grade_points = {"ＡＡ": 4.0, "Ａ": 3.0, "Ｂ": 2.0, "Ｃ": 1.0}
        if grade in grade_points:
            return grade_points[grade]
        try:
            grade = float(grade)
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
        except ValueError:
            return 0.0

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0

        for index, row in self.grades.iterrows():
            credit = row["単位数"]
            grade = row["評価"]
            gpa_target = row["GPA対象"]
            gpa_score = self.grade_to_gpa(grade)
            self.grades.at[index, "GPA換算値"] = gpa_score
            if gpa_target == "○" and grade != "／":
                total_points += credit * gpa_score
                total_credits += credit

        gpa = total_points / total_credits if total_credits > 0 else 0
        return gpa, total_credits, self.grades
