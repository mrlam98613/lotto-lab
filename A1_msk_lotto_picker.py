# msk_lotto_filter.py
import pandas as pd
import random
from datetime import datetime
from pathlib import Path
import os

# 匯入路徑與參數設定
from A0_config import DATA_DIR, history_lotto_CSV,new_pred_CSV, history_picks_CSV, MMM_TOLERANCE, TRIES, PICKS_PER_RUN, FREQ_THRESHOLD

# 匯入下一期開獎日模組（假設提供 next_draw_date, week）
import res_JC_next_drawDate
import TTsPyttsx3_BGM

# 基本號碼分類
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
ALL_NUMBERS = set(range(1, 50))
NON_PRIMES = list(ALL_NUMBERS - PRIMES)

# 資料讀取
def load_history(n_recent=30):
    df = pd.read_csv(history_lotto_CSV) # 過去開號
    df = df.sort_values("ndate").reset_index(drop=True)
    return df.tail(n_recent)

# 分析最近MMM
def calculate_mmm(nums):
    return min(nums), max(nums), int(sum(nums) / len(nums))

# 高頻非質數球號
def get_high_freq_non_primes(df, non_primes, recent_n=7, threshold=2):
    recent = df.tail(recent_n)
    all_numbers = recent[[f"N{i}" for i in range(1, 8)]].values.flatten()
    counts = pd.Series(all_numbers).value_counts()
    return [n for n in counts.index if n in non_primes and counts[n] >= threshold]

# 比對是否重複過多歷史組合
def is_similar_to_history(pick, history_df, max_overlap=5):
    pick_set = set(pick)
    for _, row in history_df.iterrows():
        hist_nums = {row[f"N{i}" ] for i in range(1,8)}
        if len(pick_set & hist_nums) >= max_overlap:
            return True
    return False

# 過濾生成號碼組合
def generate_lucky_picks(freq_non_primes, target_mmm, history_df, tolerance=(3,5,4), 
                         tries=300, picks=2):
    picks_list = []
    for _ in range(tries):
        pick = sorted(random.sample(freq_non_primes, 6))
        m, M, mean = calculate_mmm(pick)
        if not (target_mmm[0] - tolerance[0] <= m <= target_mmm[0] + tolerance[0]):
            continue
        if not (target_mmm[1] - tolerance[1] <= M <= target_mmm[1] + tolerance[1]):
            continue
        if not (target_mmm[2] - tolerance[2] <= mean <= target_mmm[2] + tolerance[2]):
            continue
        if is_similar_to_history(pick, history_df):
            continue
        picks_list.append(pick)
        if len(picks_list) == picks:
            break
    return picks_list

# 儲存結果（加上之前 next_draw_date）
def save_add_picks(picks, draw_date):
    header = "next_draw_date,N1,N2,N3,N4,N5,N6"
    file_exists = os.path.exists(new_pred_CSV)
    
    with open(new_pred_CSV, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write(header + "\n")
            
        for pick in picks:
            line = f"{draw_date}," + ",".join(map(str, pick)) + "\n"
            f.write(line)

# 儲存結果（每次覆蓋，寫入新的 next_draw_date 和 picks）
def save_picks(picks, draw_date):
    header = "next_draw_date,N1,N2,N3,N4,N5,N6"
    file_exists = os.path.exists(new_pred_CSV)
    
    with open(new_pred_CSV, "w", encoding="utf-8") as f:  # "w" 表示覆蓋

        f.write(header + "\n") 
        # 新增預測
        for pick in picks:
            line = f"{draw_date}," + ",".join(map(str, pick)) + "\n"
            f.write(line)

# 主程式
if __name__ == "__main__":
    df = load_history()
    recent = df.tail(3)
    combined_nums = recent[[f"N{i}" for i in range(1, 8)]].values.flatten()
    target_mmm = calculate_mmm(combined_nums)
    high_freq_non_primes = get_high_freq_non_primes(df, NON_PRIMES, recent_n=7, threshold=FREQ_THRESHOLD)

    lucky_combos = generate_lucky_picks(high_freq_non_primes, target_mmm, df, 
                                        tolerance=MMM_TOLERANCE, 
                                        tries=TRIES, picks=PICKS_PER_RUN)

    # 下期投注日期。
    next_draw_date, week = res_JC_next_drawDate.main()
    
    
    print(f"\n下一期開獎日期：{next_draw_date}（星期 {week}）")

    if lucky_combos:
        print("\n🎯 今日幸運單式推薦：")
        for i, pick in enumerate(lucky_combos, 1):
            print(f"注{i} {next_draw_date}：{pick}")
            
        save_picks(lucky_combos, next_draw_date)
        
        # 如果成功預測，朗讀
        TTsPyttsx3_BGM.main()
    else:
        print("⚠️ 無法生成符合條件的號碼組合。請放寬條件或重試。")
    
    
