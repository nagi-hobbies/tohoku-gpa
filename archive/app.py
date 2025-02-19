import sys

import pandas as pd
import streamlit as st

import archive.gpa as gpa

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

st.write("計算結果が表示されないときはボタンを押してください")
st.button("計算")  # ダミー：text_areaを非アクティブにするため

if text:
    try:
        df_grade = gpa.text2df(text)
        flt = df_grade["GPA換算成績"] >= 0.5
    except gpa.MyValueError as e:
        st.write("成績の形式がおかしいようです")
        st.write("エラー場所：", e.line)
        st.stop()

    st.write("---")

    st.header("GPA計算結果")
    total_credits = df_grade["単位"].sum()
    total_get_credits = df_grade[flt]["単位"].sum()
    gpa_result = sum(df_grade["GPA換算成績"] * df_grade["単位"]) / total_credits
    st.write(f"GPA:{gpa_result:.3f}")
    st.write(f"総取得単位数:{total_get_credits}")
    st.write(f"総登録単位数:{total_credits}")

    st.subheader("GPA(Grade Point Average)の計算方法")

    url = "https://www.tohoku.ac.jp/japanese/studentinfo/education/01/education0110/"
    st.write("[東北大学のGPA制度(東北大学Webサイト)](%s)" % url)
    """
    - 以下のように成績をGP(Grade Point)に換算して，単位数をかけて合計し，総取得単位数により平均をとっています。


        |5段階評価|素点|GP|
        |:---:|:---:|:---:|
        | AA | 100~90 | 4.0     |
        | A  |  89~80 | 3.0     |
        | B  |  79~70 | 2.0     |
        | C  |  69~60 | 1.0     |
        | D  |  59~   | 0.0     |



    - 履修登録後かつ成績発表前で，単位数や成績が空欄のものは，単位数0，成績0として(存在しないものとして)計算しています。
    """
    st.write("---")

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

    st.write("---")

    st.header("科目分類(大)ごとの取得単位数")
    category_credit = df_grade[flt].groupby("科目分類(大)")["単位"].sum()
    st.table(category_credit)

    st.write("---")

    st.header("科目分類(小)ごとの取得単位数")
    sub_category_credit = (
        df_grade[flt].groupby(["科目分類(大)", "科目分類(小)"])["単位"].sum()
    )
    st.table(sub_category_credit)

    st.write("---")

url = "https://github.com/nagi-hobbies/tohoku-gpa"
st.write("ソースコードはこちら [Git Hub](%s)" % url)
