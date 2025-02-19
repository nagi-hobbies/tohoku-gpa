import pandas as pd
import streamlit as st

from src.lib.gpa_calculator import GpaCalculator

st.set_page_config(
    layout="wide", page_title="Tohoku Univ GPA Calculator", page_icon="🎓"
)

st.title("Tohoku Univ GPA Calculator")

st.success(
    "2025/02/19 新学務情報システム(Universal Passport)に対応しました！",
    icon="🎉",
)

st.markdown(
    "バグ・欲しい機能等ありましたら, [X(旧Twitter)nagi](https://x.com/nagi_hobbies)までお知らせください"
)

st.header("成績画面をすべてコピー&ペースト")
st.write("Ctrl+Aで全選択、Ctrl+Cでコピー、Ctrl+VでペーストでOK")
with st.expander("うまくいかないとき.."):
    st.write("表示を下記の設定にする必要があるかもしれません")
    st.image(
        "src/assets/images/view-setting.png",
    )
    st.markdown(
        "それでもうまくいかない場合は、[X(旧Twitter)nagi](https://x.com/nagi_hobbies)までぜひお知らせください"
    )

raw_text = st.text_area(
    "↓ここにペースト↓",
    placeholder="""\
山田　太郎さん
前回ログイン：2025/02/18 14:45
setting
settingsetting

...省略...

表示
 	 科目	 単位数	 評価	 GPA対象	 年度	 学期	教員氏名
全学教育科目
全学教育基幹科目
人間論
言語表現の世界	2.0	Ａ	○	20xx	前期	池面　太郎
社会論
現代社会と法	2.0	Ａ	○	20xx	前期	半寒　次郎

...省略...
""",
    height=300,
)

if raw_text:
    try:
        calculator = GpaCalculator(raw_text)
        gpa, total_credits, df = calculator.calculate_gpa()

        st.header("計算結果")
        st.write(f"GPA: {gpa:.2f}")
        st.write(f"総取得単位数(Total Credits): {total_credits}")

        st.header("成績詳細")
        st.markdown(
            """
                    - 列名をクリックで並べ替え可能です
                    - マウスホバー時の右上メニューからCSVダウンロードが可能です
                    """
        )
        st.dataframe(df)

        # csv = df.to_csv(index=False).encode("utf-8-sig")
        # st.download_button(
        #     label="Download data as CSV",
        #     data=csv,
        #     file_name="grades.csv",
        #     mime="text/csv",
        # )

        st.header("計算方法")
        st.markdown(
            """
            - `GPA対象`が○の科目のみ計算対象としています
            - GPA換算表
                | アルファベット評価の場合 | 数値評価の場合 | GPA |
                | --- | --- | --- |
                | ＡＡ | 90以上 | 4.0 |
                | Ａ | 80以上90未満 | 3.0 |
                | Ｂ | 70以上80未満 | 2.0 |
                | Ｃ | 60以上70未満 | 1.0 |
                | それ以外 | それ以外 | 0.0 |
            """
        )

    except ValueError as e:
        st.error(f"エラー: {e}")
