# statink_player_scanner
Stat.inkの戦績を順に確認し、過去対戦したプレイヤーを探す  

# 必要なもの
- stat.inkアカウント（ログインは不要）
- 検索したいユーザ名  

# ざっくりとした処理  
- スクレイピングでプレイヤー名を抜きだす
- 探したいプレイヤー名に部分一致する場合は名前を確認し、目的の名前でなければ無視リストに追加
- 「前のバトル」ボタンからURLを探して過去の試合を総当たり

# その他スクリプト  
- statink_myscore_scanner.py：自分のキル数、塗りポイントなど各種最高記録を探す
- 最高記録：ka_max:21, kill_max:16, assist_max:12, death_max:14, sp_max:10,inked_max:2602
- 
- statink_tentamissiler_scanner.py：マルミサマンを探す
- 最高記録：0k12sp, 8k19sp
