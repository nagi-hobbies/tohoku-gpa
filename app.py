import sys

import streamlit as st

from gpa import *

st.title("Tohoku Univ GPA Calculator")
st.write("学務情報システムからコピー&ペースト(マウスでドラッグして青くするやつ)")
score_text = st.text_area(
    "↓ここにペースト↓",
    placeholder="""
全学教育科目基幹科目
     人間論
             言語表現の世界	 	  先生　太郎	  選択	  2	 	  ＡＡ	2021	  前期前半
学部専門教育科目
     理学部専門教育科目
             電磁気学Ⅰ	 	  教授　花子	  必修	  2	 	  Ｂ	2021	  後期
... (省略) ...
""",
    height=300,
)

if st.button("計算") and score_text:
    try:
        grade_data = parse_grade(score_text)
    except MyValueError as e:
        st.write("成績の形式がおかしいようです")
        # cols = re.split('[ \t]+', e.line)
        st.write("エラー場所：", e.line)
        st.stop()
    gpa, total_credits = get_gpa(grade_data[["単位数", "成績"]].values)
    st.write("GPA:{:.2f} , 総取得単位数:{}".format(gpa, total_credits))
    st.write("見出しをクリックすると並べ替えができます")
    st.dataframe(grade_data.round(2))
    st.download_button(
        label="Download .csv",
        data=grade_data.to_csv(index=False).encode("utf-8"),
        file_name="grade_data.csv",
        mime="text/csv",
    )
    st.write("Excelで文字化けする場合は文字コードをUTF-8に変更してください")
