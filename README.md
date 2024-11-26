﻿# Fortnite Discord Status

このプログラムは、**Fortniteの統計情報**を取得し、**Discordのカスタムステータス**としてリアルタイムに表示するツールです。  
キル数や勝率など、選択した統計データを1分ごとに更新しDiscordアカウントのアクティビティーに表示します

---

## 🛠 機能

- **Fortniteのリアルタイム統計情報**を取得。
- 選択可能な統計データをDiscordのアクティビティに表示（最大2項目まで）。
- **JSONファイルに設定を保存**し、次回起動時に自動読み込み。
- **エラーログ機能**：問題発生時に詳細を`log.log`に記録。
- **軽量設計**：CPUとメモリへの負荷を最小限に抑えます（確認済み：メモリ26MB、CPU約0.1％使用）。

---

## 💻 必要な環境

- **Python 3.13.0** 以降
- 必要なPythonライブラリ：
  - `requests`
  - `discordrp`
- Windows OS（`run_script.bat`で簡単実行）

---

## 🚀 使用方法

### 1. プログラムのダウンロード

1. このリポジトリをクローン、またはZIP形式でダウンロードして解凍します。
2. 解凍後、`run_script.bat`をダブルクリックして実行します。

---

### 2. 初期設定

初回起動時に、以下の情報を入力するよう求められます：

1. **DiscordアプリケーションID**  
   [Discord Developer Portal](https://discord.com/developers/applications)で作成したアプリケーションのIDを入力します。

2. **Fortnite APIキー**  
   [Fortnite API](https://fortnite-api.com/)から取得したAPIキーを入力します。

3. **Fortniteアカウント名**  
   自分のFortniteアカウント名を入力します。

4. **表示する統計データの選択**  
   以下の中から2つの統計データを選択できます：
   - 総キル数
   - 総マッチ数
   - ビクロイ数
   - 勝率
   - 平均キル数

入力した設定は、`settings.json`ファイルに保存され、次回以降は自動で読み込まれます。

---

### 3. 実行と動作確認

設定完了後、DiscordのステータスにFortniteの統計データが表示されます。データは1分ごとに更新されます。  
プログラムを終了するには、`Ctrl + C`を押してください。

---

### 4. 設定変更

設定を変更したい場合は、`settings.json`ファイルを編集するか、プログラムを再実行して設定を上書きしてください。

---

## ❓ FAQ

### Q1. このプログラムの目的は何ですか？
A1. Fortniteプレイヤーがリアルタイムの統計情報をDiscordで簡単に共有できるようにすることです。

### Q2. プログラムの負荷はどのくらいですか？
A2. 開発者のテスト環境では、**メモリ約26MB**、**CPU約0.1％**の負荷でした。使用環境によって異なる場合があります。

### Q3. エラーが発生した場合は？
A3. エラー内容は`log.log`に記録されます。このファイルを添付して以下の開発者アカウントにご連絡ください。

---

## 📧 開発者情報

- **Twitter**: [@Leakplayer](https://twitter.com/Leakplayer)  
  このプログラムの質問やバグ報告は、こちらからお気軽にご連絡ください！

---
