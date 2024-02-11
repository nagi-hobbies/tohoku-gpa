import sys

import streamlit as st

import gpa

st.title("Tohoku Univ GPA Calculator")
st.write("学務情報システムからコピー&ペースト(マウスでドラッグして青くするやつ)")
text = st.text_area(
    "↓ここにペースト↓",
    placeholder="""
HOME
教務
履修・成績
シラバス
学生支援
... (省略) ...
全学教育科目基幹科目
     人間論
             言語表現の世界	 	  先生　太郎	  選択	  2	 	  ＡＡ	2021	  前期前半
学部専門教育科目
     理学部専門教育科目
             電磁気学Ⅰ	 	  教授　花子	  必修	  2	 	  Ｂ	2021	  後期
... (省略) ...
成績照会
ｵﾝﾗｲﾝﾏﾆｭｱﾙ
履修カルテ

PAGE TOP

""",
    height=300,
)

if st.button("計算") and text:
    try:
        df_grade = gpa.text2df(text)
    except gpa.MyValueError as e:
        st.write("成績の形式がおかしいようです")
        st.write("エラー場所：", e.line)
        st.stop()
    # file_name = "grade_pc.txt"
    # with open(file_name, "r", encoding="utf-8") as f:
    #     txt_grade = f.read()
    # df_grade =new.text2df(txt_grade)
    total_credits = df_grade["単位"].sum()
    gpa = sum(df_grade["GPA換算成績"] * df_grade["単位"]) / total_credits

    category_credit = df_grade.groupby("科目分類(大)")["単位"].sum()
    sub_category_credit = df_grade.groupby(["科目分類(大)", "科目分類(小)"])["単位"].sum()

    st.header("GPA計算結果")
    st.write("GPA:{:.2f} , 総取得単位数:{}".format(gpa, total_credits))
    st.write("履修登録後かつ成績発表前で，単位数や成績が空欄のものは，単位数0，成績0として(存在しないものとして)計算しています。")

    st.header("科目分類(大)ごとの単位数")
    st.table(category_credit)
    st.header("科目分類(小)ごとの単位数")
    st.table(sub_category_credit)

    st.header("成績データ")
    st.write("見出しをクリックすると並べ替えができます")
    st.dataframe(df_grade)
    
    st.download_button(
        label="Download .csv",
        data=df_grade.to_csv(index=False),
        file_name="grade_data.csv",
        mime="text/csv",
    )
    st.write("Excelで文字化けする場合は文字コードをUTF-8に変更してください")
url = "https://github.com/nagi-hobbies/tohoku-gpa"
st.write("ソースコードはこちら [Git Hub](%s)" % url)
