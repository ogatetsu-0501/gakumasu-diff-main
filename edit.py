import yaml
import csv
import os
import re

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# YAMLファイルを読み込む関数
def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# support_triger.csvを読み込む関数
def read_support_triger(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['value']: row['trigger'] for row in reader}

# 初期リスト作成
support_card_data = read_yaml(os.path.join(current_dir, 'SupportCard.yaml'))
support_card_list = []
support_triger_data = read_support_triger(os.path.join(current_dir, 'support_triger.csv'))

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
        type_file_path = os.path.join(current_dir, f"{card['type']}.yaml")
        type_data = read_yaml(type_file_path)

        # idが一致するデータグループを探す
        matching_groups = [group for group in type_data if group['supportCardId'] == card['id']]
        
        # orderの小さい順にソート
        matching_groups.sort(key=lambda x: x['order'])
        
        for group in matching_groups:
            updated_card = {
                'supportCardOrder': card['order'],
                'name': card['name'],
                'rarity': card['rarity'],
                'type': card['type'].replace('SupportCardProduceSkillLevel', ''),
                'produceSkillOrder': group['order'],
                'supportCardLevel': group['supportCardLevel'],
                'produceSkillId': group['produceSkillId'],
                'produceSkillLevel': group['produceSkillLevel'],
                'id': card['id']
            }
            updated_list.append(updated_card)
    
    return updated_list

# ProduceSkill.yamlからdescriptionsのtextを追加
def add_description_texts(support_card_list):
    produce_skill_data = read_yaml(os.path.join(current_dir, 'ProduceSkill.yaml'))

    for card in support_card_list:
        for skill in produce_skill_data:
            if skill['id'] == card['produceSkillId'] and skill['level'] == card['produceSkillLevel']:
                texts = ' '.join([desc['text'] for desc in skill['descriptions']])
                card['text'] = texts
                card['param'] = ', '.join(re.findall(r'\d+', texts))
                card['produceEffectId1'] = skill['produceEffectId1']
                card['produceTriggerId1'] = skill['produceTriggerId1']
                card['activationRatePermil1'] = skill['activationRatePermil1']
                card['produceEffectId2'] = skill['produceEffectId2']
                card['produceTriggerId2'] = skill['produceTriggerId2']
                card['activationRatePermil2'] = skill['activationRatePermil2']
                card['produceEffectId3'] = skill['produceEffectId3']
                card['produceTriggerId3'] = skill['produceTriggerId3']
                card['activationRatePermil3'] = skill['activationRatePermil3']
                break

# ProduceEventSupportCard.yamlからproduceStepEventDetailIdを追加
def add_event_step_details(support_card_list):
    event_support_card_data = read_yaml(os.path.join(current_dir, 'ProduceEventSupportCard.yaml'))
    step_event_detail_data = read_yaml(os.path.join(current_dir, 'ProduceStepEventDetail.yaml'))

    for card in support_card_list:
        # ProduceEventSupportCard.yamlからsupportCardIdがcard['id']と一致するデータを探す
        event_groups = [group for group in event_support_card_data if group['supportCardId'] == card['id']]
        produce_effect_ids = []

        for event_group in event_groups:
            detail_id = event_group['produceStepEventDetailId']
            for step_detail in step_event_detail_data:
                if step_detail['id'] == detail_id:
                    produce_effect_ids.extend(step_detail['produceEffectIds'])

        for idx, effect_id in enumerate(produce_effect_ids):
            card[f'EventproduceEffectIds{idx+1}'] = effect_id

# support_triger.csvの値に基づいて変換
def convert_with_support_triger(value):
    if value:
        trigger_key = value[:-9]  # 下9桁を削除
        return support_triger_data.get(trigger_key, value)
    return value

# produceEffectId1の下4桁を取得
def get_effect_buf(value):
    try:
        if value:
            return int(value[-4:])
    except ValueError:
        return None
    return None

# support_card_listの更新
def update_support_card_list(support_card_list):
    for card in support_card_list:
        # produceEffectId1列の変換
        card['produceEffectId1'] = convert_with_support_triger(card.get('produceEffectId1'))

        # produceTriggerId1列の変換
        card['produceTriggerId1'] = support_triger_data.get(card.get('produceTriggerId1'), card.get('produceTriggerId1'))

        # Effectbuf列の作成
        card['Effectbuf'] = get_effect_buf(card.get('produceEffectId1'))

        # Eventbuf1およびEventeffect1の作成
        if card['rarity'] == 'SupportCardRarity_R':
            card['Eventbuf1'] = get_effect_buf(card.get('EventproduceEffectIds1'))
            card['Eventeffect1'] = convert_with_support_triger(card.get('EventproduceEffectIds1'))
            card['Eventbuf2'] = get_effect_buf(card.get('EventproduceEffectIds2'))
            card['Eventeffect2'] = convert_with_support_triger(card.get('EventproduceEffectIds2'))
        elif card['rarity'] in ['SupportCardRarity_Sr', 'SupportCardRarity_Ssr']:
            card['Eventbuf1'] = get_effect_buf(card.get('EventproduceEffectIds2'))
            card['Eventeffect1'] = convert_with_support_triger(card.get('EventproduceEffectIds2'))
            if card['rarity'] == 'SupportCardRarity_Ssr':
                card['Eventeffect2'] = support_triger_data.get(card.get('EventproduceEffectIds3'), card.get('EventproduceEffectIds3'))

        # itemcard列の作成
        if card['rarity'] in ['SupportCardRarity_Sr', 'SupportCardRarity_Ssr']:
            card['itemcard'] = support_triger_data.get(card.get('EventproduceEffectIds1'), card.get('EventproduceEffectIds1'))

# リストをCSVに出力
def export_to_csv(support_card_list, output_file):
    # CSVのヘッダーに含めるキーを動的に取得
    keys = ['rarity', 'type', 'name', 'supportCardOrder', 'produceSkillOrder', 'supportCardLevel', 'text', 
            'produceEffectId1', 'produceTriggerId1', 'activationRatePermil1', 
            'produceEffectId2', 'produceTriggerId2', 'activationRatePermil2', 
            'produceEffectId3', 'produceTriggerId3', 'activationRatePermil3',
            'Effectbuf', 'Eventbuf1', 'Eventeffect1', 'Eventbuf2', 'Eventeffect2', 'itemcard']
    
    # 動的に追加されたEventproduceEffectIdsの列を追加
    max_event_effects = max(len([key for key in card.keys() if 'EventproduceEffectIds' in key]) for card in support_card_list)
    for i in range(1, max_event_effects + 1):
        keys.append(f'EventproduceEffectIds{i}')
    
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as output_file:  # UTF-8 BOM付き
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for card in support_card_list:
            # 不要なキーを削除してから書き込む
            filtered_card = {key: card[key] for key in keys if key in card}
            dict_writer.writerow(filtered_card)

# 変換を行う関数
def transform_support_card_list(support_card_list):
    type_mapping = {
        'Visual': 'ビジュアル',
        'Vocal': 'ボーカル',
        'Dance': 'ダンス'
    }

    rarity_mapping = {
        'SupportCardRarity_R': 'R',
        'SupportCardRarity_Sr': 'SR',
        'SupportCardRarity_Ssr': 'SSR'
    }

    for card in support_card_list:
        card['type'] = type_mapping.get(card['type'], card['type'])
        card['rarity'] = rarity_mapping.get(card['rarity'], card['rarity'])
        card['supportCardLevel'] = f"Lv{card['supportCardLevel']}"

# メイン処理
updated_support_card_list = update_list_with_produce_skill(support_card_list)
add_description_texts(updated_support_card_list)
add_event_step_details(updated_support_card_list)
update_support_card_list(updated_support_card_list)
transform_support_card_list(updated_support_card_list)
export_to_csv(updated_support_card_list, os.path.join(current_dir, 'output.csv'))

print("CSVファイルが生成されました。")
