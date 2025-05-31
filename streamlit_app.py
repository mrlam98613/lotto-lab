# streamlit_app.py
import streamlit as st
import pandas as pd
# ---Streamlit
from streamlit.web import cli as stcli
from streamlit import runtime
# --cairosvg
# sys
import sys
import io
# --config
from pathlib import Path
from A0_config import new_pred_CSV, BALL_IMG_DIR, AUDIO_DIR
# --audio

import TTsPyttsx3_BGM
def main():
    st.set_page_config(page_title="六合彩推薦", layout="wide")
    st.title("🎯 今日六合彩推薦組合")

    # 讀取最新推薦號碼
    try:
        df = pd.read_csv(new_pred_CSV)
        latest = df.tail(1).iloc[0]
        draw_date = latest["next_draw_date"]
        numbers = [int(latest[f"N{i}"]) for i in range(1, 7)]

        st.subheader(f"📅 下期開獎日：{draw_date}")
        cols = st.columns(6)
        # for i, num in enumerate(numbers):
        #     with cols[i]:
        #         st.image(BALL_IMG_DIR / f"{num}.svg", caption=str(num), use_column_width=True)
        #         st.image(ball_path, width=60)  # 調整圖片寬度（單位：像素）
        
        cols = st.columns(6)
        for i, num in enumerate(numbers):
            with cols[i]:
                ball_path = BALL_IMG_DIR / f"{num}.svg"
                st.image(ball_path, width=100)
                # st.markdown(f"<img src='{ball_path}' width='100' style='display: block; margin-left: auto; margin-right: auto;'>", unsafe_allow_html=True)




    except Exception as e:
        st.error(f"⚠️ 無法載入推薦資料：{e}")
    
if __name__ == "__main__":
    
    if runtime.exists():
        main()
        TTsPyttsx3_BGM.main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
    

