import streamlit as st
import pandas as pd
from pathlib import Path
import sys
# import cairosvg
from A0_config import new_pred_CSV, BALL_IMG_DIR

def main():
    st.set_page_config(page_title="六合彩推薦", layout="wide")
    st.title("🎯 今日六合彩推薦組合")

    try:
        df = pd.read_csv(new_pred_CSV)
        latest = df.tail(1).iloc[0]
        draw_date = latest["next_draw_date"]
        numbers = [int(latest[f"N{i}"]) for i in range(1, 7)]

        st.subheader(f"📅 下期開獎日：{draw_date}")
        cols = st.columns(6)

        for i, num in enumerate(numbers):
            with cols[i]:
                # svg_path = BALL_IMG_DIR / f"{num}.svg"
                # png_path = BALL_IMG_DIR / f"temp_{num}.png"
                ball_path = BALL_IMG_DIR / f"{num}.png"

                if ball_path.exists():
                    # 轉換 SVG → PNG
                    # cairosvg.svg2png(url=str(balls_path), write_to=str(png_path))
                    st.image(str(ball_path), width=60)
                else:
                    st.warning(f"❌ 找不到球圖：{ball_path.name}")

    except Exception as e:
        st.error(f"⚠️ 無法載入推薦資料：{e}")

if __name__ == "__main__":
    if hasattr(st, "runtime") and st.runtime.exists():
        main()
    else:
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
