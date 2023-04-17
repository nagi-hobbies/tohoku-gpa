import streamlit as st
import pandas as pd


def can_convert_to_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parse_grade(grade_text):
    grade_list = []
    lines = grade_text.split('\n')
    for line in lines:
        cols = line.split()
        if len(cols) >= 5:
            name = cols[0]
            grade = str(cols[-3])
            if can_convert_to_float(cols[-4]):
                credits = float(cols[-4])
            else:
                grade = str(cols[-4]) + grade
                credits = float(cols[-5])
            grade_list.append([name, credits, grade])
    grade_data = pd.DataFrame(grade_list, columns=['教科名', '単位数', '成績'])
    return grade_data


def get_gpa(ug_arr):
    """
    ug_arr: 2次元配列，単位数と成績の配列
    """
    gpa = 0
    total_credits = 0
    for ug in ug_arr:
        credits = ug[0]
        grade = ug[1]
        if grade == 'ＡＡ':
            gpa += 4 * credits
        elif grade == 'Ａ':
            gpa += 3 * credits
        elif grade == 'Ｂ':
            gpa += 2 * credits
        elif grade == 'Ｃ':
            gpa += 1 * credits
        elif grade == 'Ｄ':
            gpa += 0 * credits
        total_credits += credits
    gpa = gpa / total_credits
    return gpa, total_credits


st.title('Tohoku Uni GPA Calculator')
st.write('学務情報システムからコピー&ペースト(マウスでドラッグして青くするやつ)')
score_text = st.text_area("↓ここにペースト↓", placeholder="""
全学教育科目基幹科目
     人間論
             教科名	 	  鈴木　太郎	  選択	  2	 	  ＡＡ	2021	  前期前半
... (省略) ...
""")
if st.button('計算') and score_text:
    grade_data = parse_grade(score_text)
    gpa, total_credits = get_gpa(grade_data[['単位数', '成績']].values)
    st.write('あなたのGPAは {:.2f} (総取得単位数{})'.format(gpa, total_credits))
    st.dataframe(grade_data.round(2))
    st.download_button(
        label='Download .csv',
        data=grade_data.to_csv(index=False).encode('utf-8'),
        file_name='grade_data.csv',
        mime='text/csv'
    )
    st.write('文字化けする場合は文字コードをUTF-8に変更してください')
