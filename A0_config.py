# config.py
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"

AUDIO_DIR = ROOT_DIR / "audio_folder"
BALL_IMG_DIR = ROOT_DIR / "msk_balls"
# ---
history_lotto_CSV = DATA_DIR / "M2_lotto_history.csv"
new_pred_CSV = DATA_DIR / "B1_new_pred_picks.csv"
history_picks_CSV = DATA_DIR / "B2_history_picks.csv"

MMM_TOLERANCE = (3, 5, 4)       # 最小號 ±3, 最大 ±5, 平均 ±4
TRIES = 10000                   # 嘗試生成組合次數
PICKS_PER_RUN = 2              # 每次生成注數
FREQ_THRESHOLD = 2             # 高頻球出現次數門檻



'''
模仿最近期型號（穩健）	(3, 5, 4)	維持和最近期結構相似
更保守集中型（高重複）	(2, 4, 3)	篩選更嚴格、結果更少
增加組合多樣性	(5, 8, 6)	結構彈性大、增加變化


追求穩定、常出現號碼	threshold=3	只取常見號碼
保守但增加彈性	threshold=2	目前你用的值
更開放選號來源	threshold=1	幾乎所有號碼都有機會選入


'''
