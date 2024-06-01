import csv
import yaml
import os

# 現在のディレクトリを取得
current_directory = os.path.dirname(__file__)

# ファイルパスを設定
idol_card_path = os.path.join(current_directory, 'IdolCard.yaml')
character_path = os.path.join(current_directory, 'Character.yaml')
idol_card_potential_path = os.path.join(current_directory, 'IdolCardPotential.yaml')
character_true_end_bonus_path = os.path.join(current_directory, 'CharacterTrueEndBonus.yaml')
character_dearness_level_path = os.path.join(current_directory, 'CharacterDearnessLevel.yaml')
produce_step_audition_difficulty_path = os.path.join(current_directory, 'ProduceStepAuditionDifficulty.yaml')
produce_exam_battle_config_path = os.path.join(current_directory, 'ProduceExamBattleConfig.yaml')

# YAMLファイルの読み込み
with open(idol_card_path, 'r', encoding='utf-8') as f:
    idol_card_data = yaml.safe_load(f)

with open(character_path, 'r', encoding='utf-8') as f:
    character_data = yaml.safe_load(f)

with open(idol_card_potential_path, 'r', encoding='utf-8') as f:
    idol_card_potential_data = yaml.safe_load(f)

with open(character_true_end_bonus_path, 'r', encoding='utf-8') as f:
    character_true_end_bonus_data = yaml.safe_load(f)

with open(character_dearness_level_path, 'r', encoding='utf-8') as f:
    character_dearness_level_data = yaml.safe_load(f)

with open(produce_step_audition_difficulty_path, 'r', encoding='utf-8') as f:
    produce_step_audition_difficulty_data = yaml.safe_load(f)

with open(produce_exam_battle_config_path, 'r', encoding='utf-8') as f:
    produce_exam_battle_config_data = yaml.safe_load(f)

# キャラクターの辞書を作成
character_dict = {char['id']: char for char in character_data}

# ポテンシャルの辞書を作成
idol_card_potential_dict = {}
for potential in idol_card_potential_data:
    if potential['id'] not in idol_card_potential_dict:
        idol_card_potential_dict[potential['id']] = []
    idol_card_potential_dict[potential['id']].append(potential)

# TrueEndBonusの辞書を作成
character_true_end_bonus_dict = {bonus['id']: bonus for bonus in character_true_end_bonus_data}

# DearnessLevelの辞書を作成
character_dearness_level_dict = {}
for dearness in character_dearness_level_data:
    if dearness['characterId'] not in character_dearness_level_dict:
        character_dearness_level_dict[dearness['characterId']] = []
    character_dearness_level_dict[dearness['characterId']].append(dearness)

# ProduceStepAuditionDifficultyの辞書を作成
produce_step_audition_difficulty_dict = {}
for item in produce_step_audition_difficulty_data:
    if item['id'] not in produce_step_audition_difficulty_dict:
        produce_step_audition_difficulty_dict[item['id']] = []
    produce_step_audition_difficulty_dict[item['id']].append(item)

# ProduceExamBattleConfigの辞書を作成
produce_exam_battle_config_dict = {item['id']: item for item in produce_exam_battle_config_data}

# CSVファイルのヘッダーを作成
headers = [
    'id', 'name', 'order', 'planType', 'produceDance', 'produceDanceGrowthRatePermil',
    'produceStamina', 'produceStepAuditionDifficultyId', 'produceVisual',
    'produceVisualGrowthRatePermil', 'produceVocal', 'produceVocalGrowthRatePermil',
    'rarity', 'idolCardLevelLimitStatusUpId', 'idolCardPotentialId',
    'MidforceEndScore', 'MidbaseScore', 'Midvocalbolder', 'Middancebolder', 'Midvisualbolder',
    'FinalforceEndScore', 'FinalbaseScore', 'Finalvocalbolder', 'Finaldancebolder', 'Finalvisualbolder'
]

# ポテンシャルのデータに基づいてヘッダーを追加
for potential in idol_card_potential_data:
    rank = potential['rank'].replace("IdolCardPotentialRank__", "")
    headers.append(f'{rank}ProduceDanceGrowthRatePermil')
    headers.append(f'{rank}ProduceVisualGrowthRatePermil')
    headers.append(f'{rank}ProduceVocalGrowthRatePermil')
    headers.append(f'{rank}EffectValue')

# TrueEndBonusとDearnessLevelのヘッダーを追加
headers.extend([
    'trueProduceDance', 'trueProduceDanceGrowthRatePermil', 'trueProduceStamina',
    'trueProduceVisual', 'trueProduceVisualGrowthRatePermil', 'trueProduceVocal', 'trueProduceVocalGrowthRatePermil'
])
dearness_levels = set()
for dearness in character_dearness_level_data:
    dearness_levels.add(dearness["dearnessLevel"])
for level in sorted(dearness_levels):
    headers.append(f'dearness{level}')

# 重複したヘッダーを削除
headers = list(dict.fromkeys(headers))

# リスト1のデータを作成
list1_data = []
for card in idol_card_data:
    character_id = card['characterId']
    if character_id in character_dict:
        character = character_dict[character_id]
        card['id'] = f"{character['lastName']}{character['firstName']}"
        
        # TrueEndBonusの取得
        true_end_bonus = character_true_end_bonus_dict.get(character.get('characterTrueEndBonusId', ''), {})
        true_end_data = {
            'trueProduceDance': true_end_bonus.get('produceDance', ''),
            'trueProduceDanceGrowthRatePermil': true_end_bonus.get('produceDanceGrowthRatePermil', ''),
            'trueProduceStamina': true_end_bonus.get('produceStamina', ''),
            'trueProduceVisual': true_end_bonus.get('produceVisual', ''),
            'trueProduceVisualGrowthRatePermil': true_end_bonus.get('produceVisualGrowthRatePermil', ''),
            'trueProduceVocal': true_end_bonus.get('produceVocal', ''),
            'trueProduceVocalGrowthRatePermil': true_end_bonus.get('produceVocalGrowthRatePermil', '')
        }

        # DearnessLevelの取得
        dearness_data = {f'dearness{level}': '' for level in dearness_levels}
        if character_id in character_dearness_level_dict:
            for dearness in character_dearness_level_dict[character_id]:
                level = dearness['dearnessLevel']
                for skill in dearness['produceSkills']:
                    if skill['id'] == 'p_dearness_skill-common-p_trigger-produce_start-no_description-audition_parameter_bonus_multiple-03-001':
                        dearness_data[f'dearness{level}'] = skill.get('level', '')

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

    # ProduceStepAuditionDifficultyの取得とフィルタリング
    produce_step_id = card['produceStepAuditionDifficultyId']
    mid_data = {}
    final_data = {}
    if produce_step_id in produce_step_audition_difficulty_dict:
        difficulties = produce_step_audition_difficulty_dict[produce_step_id]
        # Mid条件でフィルタリング
        mid_filtered = [d for d in difficulties if d['produceId'] == 'produce-002' and d['stepType'] == 'ProduceStepType_AuditionMid1']
        if mid_filtered:
            mid_filtered = mid_filtered[0]  # 1つだけ使用
            mid_data['MidforceEndScore'] = mid_filtered.get('forceEndScore', '')
            mid_data['MidbaseScore'] = mid_filtered.get('baseScore', '')
            produce_exam_battle_id = mid_filtered.get('produceExamBattleConfigId', '')
            if produce_exam_battle_id in produce_exam_battle_config_dict:
                exam_config = produce_exam_battle_config_dict[produce_exam_battle_id]
                mid_data['Midvocalbolder'] = exam_config.get('vocal', '')
                mid_data['Middancebolder'] = exam_config.get('dance', '')
                mid_data['Midvisualbolder'] = exam_config.get('visual', '')

        # Final条件でフィルタリング
        final_filtered = [d for d in difficulties if d['produceId'] == 'produce-002' and d['stepType'] == 'ProduceStepType_AuditionFinal']
        if final_filtered:
            final_filtered = final_filtered[0]  # 1つだけ使用
            final_data['FinalforceEndScore'] = final_filtered.get('forceEndScore', '')
            final_data['FinalbaseScore'] = final_filtered.get('baseScore', '')
            produce_exam_battle_id = final_filtered.get('produceExamBattleConfigId', '')
            if produce_exam_battle_id in produce_exam_battle_config_dict:
                exam_config = produce_exam_battle_config_dict[produce_exam_battle_id]
                final_data['Finalvocalbolder'] = exam_config.get('vocal', '')
                final_data['Finaldancebolder'] = exam_config.get('dance', '')
                final_data['Finalvisualbolder'] = exam_config.get('visual', '')

    # rarityの変換
    rarity_conversion = {
        "IdolCardRarity_R": "R",
        "IdolCardRarity_Sr": "SR",
        "IdolCardRarity_Ssr": "SSR"
    }
    rarity_value = card.get('rarity', '')
    converted_rarity = rarity_conversion.get(rarity_value, rarity_value)

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
        'rarity': converted_rarity,
        'idolCardLevelLimitStatusUpId': card.get('idolCardLevelLimitStatusUpId', ''),
        'idolCardPotentialId': card.get('idolCardPotentialId', ''),
        **rank_data,
        **true_end_data,
        **dearness_data,
        **mid_data,
        **final_data
    })

# CSVファイルの書き込み (UTF-8 BOM形式)
csv_output_path = os.path.join(current_directory, 'IdolCardList.csv')
with open(csv_output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    writer.writerows(list1_data)

print(f'CSVファイルがUTF-8 BOM形式で正常に作成されました: {csv_output_path}')
