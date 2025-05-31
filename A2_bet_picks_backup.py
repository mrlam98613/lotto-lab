import pandas as pd
from pathlib import Path
from A0_config import new_pred_CSV, history_picks_CSV


            
def backup_predictions():
    # 讀入新預測
    if not new_pred_CSV.exists():
        print(f"❌ B1 預測檔案不存在：{new_pred_CSV}")
        return

    new_df = pd.read_csv(new_pred_CSV)

    # 若歷史檔案尚未存在，建立新檔
    if not history_picks_CSV.exists():
        
        print("📁 B2 沒有歷史投注紀錄，建立新檔...")
        
        new_df.to_csv(history_picks_CSV, index=False)
        print("✅ B1 已備份至歷史投注紀錄。")
        return

    if history_picks_CSV.stat().st_size == 0:
        print("⚠️ B2 歷史紀錄檔是空的，直接寫入預測作為第一筆紀錄。")
        new_df.to_csv(history_picks_CSV, index=False)
        return

    # 載入歷史紀錄
    history_df = pd.read_csv(history_picks_CSV)

    # 檢查是否已有相同日期的資料
    existing_dates = set(history_df["next_draw_date"])
    new_dates = set(new_df["next_draw_date"])

    overlap = existing_dates & new_dates
    if overlap:
        print(f"⚠️ B2 已存在相同日期的投注紀錄：{', '.join(overlap)}")
        print("🚫 這次不進行備份。請確認是否已經儲存過。")
        return

    # 合併並儲存
    combined_df = pd.concat([history_df, new_df], ignore_index=True)
    combined_df = combined_df.sort_values("next_draw_date").reset_index(drop=True)
    print(combined_df)
    combined_df.to_csv(history_picks_CSV, index=False)

    print(f"✅ B2 備份完成，共 {len(combined_df)} 筆歷史投注資料。")

if __name__ == "__main__":
    backup_predictions()

            

