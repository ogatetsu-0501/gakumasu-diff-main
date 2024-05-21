import yaml
import csv
import os

# YAMLファイルを読み込む関数
def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 初期リスト作成
support_card_data = read_yaml('SupportCard.yaml')
support_card_list = []

for card in support_card_data:
    name = card['name']
    id_ = card['id']
    type_ = card['type'].replace('SupportCardType_', 'SupportCardProduceSkillLevel')
    order = card['order']
    rarity = card['rarity']
    support_card_list.append({'name': name, 'id': id_, 'type': type_, 'order': order, 'rarity': rarity})

# 追加情報取得
def update_list_with_produce_skill(support_card_list):
    updated_list = []
    for card in support_card_list:
        type_file_path = f"{card['type']}.yaml"
        type_data = read_yaml(type_file_path)

        # idが一致するデータグループを探す
        matching_groups = [group for group in type_data if group['supportCardId'] == card['id']]
        
        # orderの小さい順にソート
        matching_groups.sort(key=lambda x: x['order'])
        
        for group in matching_groups:
            updated_card = {
                'supportCardOrder': card['order'],
                'name': card['name'],
                'rarity': card['rarity'].replace('SupportCardRarity_', ''),
                'type': card['type'].replace('SupportCardProduceSkillLevel', ''),
                'produceSkillOrder': group['order'],
                'supportCardLevel': group['supportCardLevel'],
                'produceSkillId': group['produceSkillId'],
                'produceSkillLevel': group['produceSkillLevel']
            }
            updated_list.append(updated_card)
    
    return updated_list

# ProduceSkill.yamlからdescriptionsのtextを追加
def add_description_texts(support_card_list):
    produce_skill_data = read_yaml('ProduceSkill.yaml')

    for card in support_card_list:
        for skill in produce_skill_data:
            if skill['id'] == card['produceSkillId'] and skill['level'] == card['produceSkillLevel']:
                texts = ' '.join([desc['text'] for desc in skill['descriptions']])
                card['text'] = texts
                break

# リストをCSVに出力
def export_to_csv(support_card_list, output_file):
    keys = ['rarity', 'type', 'name', 'supportCardOrder', 'produceSkillOrder', 'supportCardLevel', 'text']
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as output_file:  # UTF-8 BOM付き
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for card in support_card_list:
            # 不要なキーを削除してから書き込む
            filtered_card = {key: card[key] for key in keys}
            dict_writer.writerow(filtered_card)

# メイン処理
updated_support_card_list = update_list_with_produce_skill(support_card_list)
add_description_texts(updated_support_card_list)
export_to_csv(updated_support_card_list, 'output.csv')

print("CSVファイルが生成されました。")
