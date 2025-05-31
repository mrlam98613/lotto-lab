from pathlib import Path
import pandas as pd
from pydub import AudioSegment
import subprocess
import os

# === 參數設定 ===
current_dir = Path(__file__).resolve().parent
# data / new pred
csv_path = current_dir / 'data/B1_new_pred_picks.csv'

#--- audio
bgm_path = current_dir / 'audio_folder/BGMusic.mp3'
aiff_path = current_dir / "audio_folder/nextDraw.aiff"
mp3_path = current_dir / "audio_folder/nextDraw.mp3"
final_mix_path = current_dir / "audio_folder/final_mix.mp3"


# 使用語音（1：普通話，2：粵語）
voice_choice = str(1)   # 可改為 "2" 試試粵語

if voice_choice == "1":
    voice_id = "Tingting"  # ✅ 對應 say -v 中的名稱
    convert_date = False
elif voice_choice == "2":
    voice_id = "Sinji"
    convert_date = True
else:
    raise ValueError("❌ 無效的語音選擇，請輸入 '1' 或 '2'")

def format_date_for_speech(date_str):
    y, m, d = date_str.split('-')
    return f"{int(y)}年{int(m)}月{int(d)}日"

def generate_combined_text():
    df = pd.read_csv(csv_path)
    lines = [f"你的預測投注有{len(df)}注"]
    
    for i, row in df.iterrows():
        date = format_date_for_speech(str(row.iloc[0])) if convert_date else str(row.iloc[0])
        nums = '、'.join(map(str, row[1:].dropna().astype(int)))
        lines.append(f"第{i+1}注：{date}號碼,是：{nums}")
    return "。".join(lines)


def text_to_speech(text):
    voice_name = voice_id.split('.')[-1]
    print(f"🧪 使用語音：{voice_name}")  # 新增這行幫助檢查
    subprocess.run(["say", "-v", voice_name, "-o", str(aiff_path), text], check=True)
    
def convert_to_mp3():
    audio = AudioSegment.from_file(aiff_path, format="aiff")
    audio.export(mp3_path, format="mp3")

def mix_with_bgm():
    voice = AudioSegment.from_file(mp3_path)
    bgm = AudioSegment.from_file(bgm_path) - 25
    looped_bgm = (bgm * (len(voice) // len(bgm) + 1))[:len(voice)]
    combined = voice.overlay(looped_bgm)
    combined.export(final_mix_path, format="mp3")
    os.system(f'afplay "{final_mix_path}"')  # 播放

def main():
    text = generate_combined_text()
    print(f"🔊 語音內容：{text}")  # 前50字檢查
    text_to_speech(text)
    convert_to_mp3()
    mix_with_bgm()
    print(f"✅ 已輸出最終語音到：{final_mix_path}")

if __name__ == "__main__":
    main()
