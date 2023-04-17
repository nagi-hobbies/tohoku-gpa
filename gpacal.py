import chardet


def can_convert_to_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_scores(scores_str):
    grade_list = []
    lines = scores_str.split('\n')
    for line in lines:
        cols = line.split()
        # print(len(cols))
        if len(cols) >= 5:
            grade = str(cols[-3])
            if can_convert_to_float(cols[-4]):
                units = float(cols[-4])
            else:
                grade = str(cols[-4]) + grade
                units = float(cols[-5])
            grade_list.append([units, grade])
    return grade_list


def get_gpa(ug_arr):
    """
    ug_arr: 2次元配列，単位数と成績の配列
    """
    gpa = 0
    total_units = 0
    for ug in ug_arr:
        units = ug[0]
        grade = ug[1]
        if grade == 'ＡＡ':
            gpa += 4 * units
        elif grade == 'Ａ':
            gpa += 3 * units
        elif grade == 'Ｂ':
            gpa += 2 * units
        elif grade == 'Ｃ':
            gpa += 1 * units
        elif grade == 'Ｄ':
            gpa += 0 * units
        total_units += units
    gpa = gpa / total_units
    return gpa, total_units


file_name = 'grade.txt'

with open(file_name, 'rb') as f:
    result = chardet.detect(f.read())

with open(file_name, encoding=result['encoding']) as f:
    grade_text = f.read()

ug = parse_scores(grade_text)
print(ug)
gpa = get_gpa(ug)
print(gpa)
