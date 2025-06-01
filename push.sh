#!/bin/bash

# 檢查是否有輸入 commit 訊息
if [ -z "$1" ]; then
  echo "❗ 請輸入 commit 訊息，例如："
  echo "    bash push.sh \"🔧 修正預測邏輯\""
  exit 1
fi

echo "📂 Git 狀態檢查中..."
git status

echo "🗃️ 加入所有修改..."
git add .

echo "📝 提交：$1"
git commit -m "$1"

echo "🔄 拉取遠端變更（避免衝突）..."
git pull origin main --allow-unrelated-histories

echo "🚀 推送到 GitHub..."
git push

echo "✅ 推送完成！"
