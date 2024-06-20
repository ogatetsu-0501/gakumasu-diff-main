import yaml
import pandas as pd

# YAMLファイルを読み込む
with open('ProduceCard.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

# rarityの変換マッピング
rarity_mapping = {
    'ProduceCardRarity_N': 'N',
    'ProduceCardRarity_R': 'R',
    'ProduceCardRarity_Sr': 'SR',
    'ProduceCardRarity_Ssr': 'SSR'
}

# planTypeの変換マッピング
plantype_mapping = {
    'ProducePlanType_Plan1': 'センス',
    'ProducePlanType_Plan2': 'ロジック',
    'ProducePlanType_Common': 'フリー'
}

# categoryの変換マッピング
category_mapping = {
    'ProduceCardCategory_Trouble': 'トラブル',
    'ProduceCardCategory_ActiveSkill': 'アクティブ',
    'ProduceCardCategory_MentalSkill': 'メンタル'
}

# costTypeの変換マッピング
costtype_mapping = {
    'ExamCostType_Unknown': '',
    'ExamCostType_ExamLessonBuff': '集中',
    'ExamCostType_ExamParameterBuff': '好調',
    'ExamCostType_ExamCardPlayAggressive': 'やる気',
    'ExamCostType_ExamReview': '好印象'
}

# playMovePositionTypeの変換マッピング
playmovepositiontype_mapping = {
    'ProduceCardMovePositionType_Lost': 'レッスン中1回',
    'ProduceCardMovePositionType_Grave': ''
}

# isInitialの変換マッピング
isinitial_mapping = {
    True: '開始時獲得',
    False: ''
}

# noDeckDuplicationの変換マッピング
nodeckduplication_mapping = {
    True: 'デッキ内1枚',
    False: ''
}

# 抽出したデータを保持するリスト
cards = []

# 各カードのデータを抽出する
for card in data:
    rarity = card.get('rarity', '')
    converted_rarity = rarity_mapping.get(rarity, rarity)
    planType = card.get('planType', '')
    converted_planType = plantype_mapping.get(planType, planType)
    category = card.get('category', '')
    converted_category = category_mapping.get(category, category)
    costType = card.get('costType', '')
    converted_costType = costtype_mapping.get(costType, costType)
    playMovePositionType = card.get('playMovePositionType', '')
    converted_playMovePositionType = playmovepositiontype_mapping.get(playMovePositionType, playMovePositionType)
    isInitial = card.get('isInitial', False)
    converted_isInitial = isinitial_mapping.get(isInitial, isInitial)
    noDeckDuplication = card.get('noDeckDuplication', False)
    converted_noDeckDuplication = nodeckduplication_mapping.get(noDeckDuplication, noDeckDuplication)

    card_info = {
        'name': card.get('name', ''),
        'rarity': converted_rarity,
        'planType': converted_planType,
        'category': converted_category,
        'stamina': card.get('stamina', 0),
        'forceStamina': card.get('forceStamina', 0),
        'costType': converted_costType,
        'costValue': card.get('costValue', 0),
        'playProduceExamTriggerId': card.get('playProduceExamTriggerId', ''),
        'playMovePositionType': converted_playMovePositionType,
        'moveEffectTriggerType': card.get('moveEffectTriggerType', ''),
        'moveProduceExamEffectIds': card.get('moveProduceExamEffectIds', []),
        'isEndTurnLost': card.get('isEndTurnLost', False),
        'isInitial': converted_isInitial,
        'isRestrict': card.get('isRestrict', False),
        'produceCardStatusEnchantId': card.get('produceCardStatusEnchantId', ''),
        'searchTag': card.get('searchTag', ''),
        'libraryHidden': card.get('libraryHidden', False),
        'noDeckDuplication': converted_noDeckDuplication,
        'unlockProducerLevel': card.get('unlockProducerLevel', 0),
        'rentalUnlockProducerLevel': card.get('rentalUnlockProducerLevel', 0),
        'evaluation': card.get('evaluation', 0),
        'originIdolCardId': card.get('originIdolCardId', ''),
        'originSupportCardId': card.get('originSupportCardId', ''),
        'isInitialDeckProduceCard': card.get('isInitialDeckProduceCard', False),
        'effectGroupIds': card.get('effectGroupIds', []),
        'viewStartTime': card.get('viewStartTime', '0'),
        'isLimited': card.get('isLimited', False),
        'order': card.get('order', '')
    }
    
    # playEffectsの連番付き項目を追加
    for i, effect in enumerate(card.get('playEffects', []), start=1):
        card_info[f'produceExamTriggerId{i}'] = effect.get('produceExamTriggerId', '')
        card_info[f'produceExamEffectId{i}'] = effect.get('produceExamEffectId', '')
        card_info[f'hideIcon{i}'] = effect.get('hideIcon', False)
    
    cards.append(card_info)

# DataFrameに変換
df = pd.DataFrame(cards)

# CSVに出力 (UTF-8 BOM付き)
df.to_csv('ProduceCard.csv', index=False, encoding='utf-8-sig')

# データフレームを表示
print(df)
