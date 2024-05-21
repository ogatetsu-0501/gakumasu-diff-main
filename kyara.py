import csv
import yaml
import os

# 現在のディレクトリを取得
current_directory = os.path.dirname(__file__)

# ファイルパスを設定
idol_card_path = os.path.join(current_directory, 'IdolCard.yaml')
character_path = os.path.join(current_directory, 'Character.yaml')
idol_card_potential_path = os.path.join(current_directory, 'IdolCardPotential.yaml')

# YAMLファイルの読み込み
with open(idol_card_path, 'r', encoding='utf-8') as f:
    idol_card_data = yaml.safe_load(f)

with open(character_path, 'r', encoding='utf-8') as f:
    character_data = yaml.safe_load(f)

with open(idol_card_potential_path, 'r', encoding='utf-8') as f:
    idol_card_potential_data = yaml.safe_load(f)

# キャラクターの辞書を作成
character_dict = {char['id']: char for char in character_data}

# ポテンシャルの辞書を作成
idol_card_potential_dict = {}
for potential in idol_card_potential_data:
    if potential['id'] not in idol_card_potential_dict:
        idol_card_potential_dict[potential['id']] = []
    idol_card_potential_dict[potential['id']].append(potential)

# CSVファイルのヘッダーを作成
headers = [
    'id', 'name', 'order', 'planType', 'produceDance', 'produceDanceGrowthRatePermil',
    'produceStamina', 'produceStepAuditionDifficultyId', 'produceVisual',
    'produceVisualGrowthRatePermil', 'produceVocal', 'produceVocalGrowthRatePermil',
    'rarity', 'idolCardLevelLimitStatusUpId', 'idolCardPotentialId'
]

# ポテンシャルのデータに基づいてヘッダーを追加
for potential in idol_card_potential_data:
    rank = potential['rank'].replace("IdolCardPotentialRank__", "")
    headers.append(f'{rank}ProduceDanceGrowthRatePermil')
    headers.append(f'{rank}ProduceVisualGrowthRatePermil')
    headers.append(f'{rank}ProduceVocalGrowthRatePermil')
    headers.append(f'{rank}EffectValue')

# 重複したヘッダーを削除
headers = list(dict.fromkeys(headers))

# リスト1のデータを作成
list1_data = []
for card in idol_card_data:
    character_id = card['characterId']
    if character_id in character_dict:
        character = character_dict[character_id]
        card['id'] = f"{character['lastName']}{character['firstName']}"

    potential_id = card['idolCardPotentialId']
    rank_data = {}
    if potential_id in idol_card_potential_dict:
        potentials = idol_card_potential_dict[potential_id]
        for potential in potentials:
            rank = potential['rank'].replace("IdolCardPotentialRank__", "")
            rank_data[f'{rank}ProduceDanceGrowthRatePermil'] = potential.get('produceDanceGrowthRatePermil', '')
            rank_data[f'{rank}ProduceVisualGrowthRatePermil'] = potential.get('produceVisualGrowthRatePermil', '')
            rank_data[f'{rank}ProduceVocalGrowthRatePermil'] = potential.get('produceVocalGrowthRatePermil', '')
            rank_data[f'{rank}EffectValue'] = potential.get('effectValue', '')

    list1_data.append({
        'id': card['id'],
        'name': card.get('name', ''),
        'order': card.get('order', ''),
        'planType': card.get('planType', ''),
        'produceDance': card.get('produceDance', ''),
        'produceDanceGrowthRatePermil': card.get('produceDanceGrowthRatePermil', ''),
        'produceStamina': card.get('produceStamina', ''),
        'produceStepAuditionDifficultyId': card.get('produceStepAuditionDifficultyId', ''),
        'produceVisual': card.get('produceVisual', ''),
        'produceVisualGrowthRatePermil': card.get('produceVisualGrowthRatePermil', ''),
        'produceVocal': card.get('produceVocal', ''),
        'produceVocalGrowthRatePermil': card.get('produceVocalGrowthRatePermil', ''),
        'rarity': card.get('rarity', ''),
        'idolCardLevelLimitStatusUpId': card.get('idolCardLevelLimitStatusUpId', ''),
        'idolCardPotentialId': card.get('idolCardPotentialId', ''),
        **rank_data
    })

# CSVファイルの書き込み (UTF-8 BOM形式)
csv_output_path = os.path.join(current_directory, 'IdolCardList.csv')
with open(csv_output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(list1_data)

print(f'CSVファイルがUTF-8 BOM形式で正常に作成されました: {csv_output_path}')
