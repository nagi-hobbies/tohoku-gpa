import sys
import streamlit as st
import pandas as pd
import re


class MyValueError(Exception):
    def __init__(self, line):
        self.line = line
    pass


def parse_grade(grade_text):
    grade_list = []
    main_category = ''
    sub_category = ''
    lines = grade_text.split('\n')
    for line in lines:
        cols = re.split('[ \t]+', line)
        if len(cols) == 1:
            main_category = cols[0]
        elif len(cols) == 2:
            sub_category = cols[1]
        elif len(cols) == 8:
            cols[-2] = int(cols[-2])
            cols[-4] = float(cols[-4])
            grade_list.append([main_category, sub_category, *cols[1:]])
        else:
            raise MyValueError(line)
    grade_data = pd.DataFrame(
        grade_list,
        columns=['科目分類(大)',
                 '科目分類(小)',
                 '教科名',
                 '教授名',
                 '選択or必修or?',
                 '単位数',
                 '成績',
                 '取得年度',
                 '前期or後期'])
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
        if grade == 'ＡＡ':
            gpa += 4 * crdt
        elif grade == 'Ａ':
            gpa += 3 * crdt
        elif grade == 'Ｂ':
            gpa += 2 * crdt
        elif grade == 'Ｃ':
            gpa += 1 * crdt
        else:
            continue
        total_credits += crdt
    gpa = gpa / total_credits
    return gpa, total_credits


st.title('Tohoku Univ GPA Calculator')
st.write('学務情報システムからコピー&ペースト(マウスでドラッグして青くするやつ)')
score_text = st.text_area("↓ここにペースト↓", placeholder="""
全学教育科目基幹科目
     人間論
             言語表現の世界	 	  先生　太郎	  選択	  2	 	  ＡＡ	2021	  前期前半
学部専門教育科目
     理学部専門教育科目
             電磁気学Ⅰ	 	  松原　正和	  必修	  2	 	  Ｂ	2021	  後期
... (省略) ...
""", height=300)

if st.button('計算') and score_text:

    try:
        grade_data = parse_grade(score_text)
    except MyValueError as e:
        st.write('成績の形式がおかしいようです')
        st.write('エラー場所：',e.line)
        st.stop()
    gpa, total_credits = get_gpa(grade_data[['単位数', '成績']].values)
    st.write('GPA:{:.2f} , 総取得単位数:{}'.format(gpa, total_credits))
    st.write('見出しをクリックすると並べ替えができます')
    st.dataframe(grade_data.round(2))
    st.download_button(
        label='Download .csv',
        data=grade_data.to_csv(index=False).encode('utf-8'),
        file_name='grade_data.csv',
        mime='text/csv'
    )
    st.write('Excelで文字化けする場合は文字コードをUTF-8に変更してください')
