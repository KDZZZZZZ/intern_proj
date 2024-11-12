import numpy as np

# 定义权重
WEIGHTS = {
    'personality': 0.3,
    'mood': 0.2,
    'affinity': 0.3,
    'topic_relevance': 0.2
}

# 阈值设定
THRESHOLD = 0.6

def normalize(vector):
    """标准化向量到0-1范围"""
    min_val = np.min(vector)
    max_val = np.max(vector)
    if max_val - min_val == 0:
        return np.zeros_like(vector)
    return (vector - min_val) / (max_val - min_val)

def personality_score(personality_traits, topic_personality_weights):
    """
    计算人格特质对话题的适配度
    :param personality_traits: dict, 包含五大人格特质分数
    :param topic_personality_weights: dict, 各特质对话题的权重
    :return: float, 人格特质评分
    """
    score = 0
    for trait in personality_traits:
        score += personality_traits[trait] * topic_personality_weights.get(trait, 0)
    # 标准化
    return normalize(np.array([score]))[0]

def mood_score(mood_vad, topic_mood_effect):
    """
    计算情感状态对话题的适配度
    :param mood_vad: dict, Valence, Arousal, Dominance分数
    :param topic_mood_effect: dict, 每个VAD维度对话题的影响权重
    :return: float, 情感状态评分
    """
    score = 0
    for dim in mood_vad:
        score += mood_vad[dim] * topic_mood_effect.get(dim, 0)
    # 标准化
    return normalize(np.array([score]))[0]

def calculate_topic_activation(personality, personality_weights, mood, mood_effect,
                               affinity, 
                               #topic_relevance
                               ):
    """
    计算是否激发话题
    :param personality: dict, 五大人格特质分数
    :param personality_weights: dict, 各人格特质对话题的权重
    :param mood: dict, VAD分数
    :param mood_effect: dict, VAD对话题的影响权重
    :param affinity: float, 好感度分数（0-1）
    :param topic_relevance: float, 话题关联度分数（0-1）
    :return: bool, 是否激发话题
    """
    # 计算各部分得分
    p_score = personality_score(personality, personality_weights)
    m_score = mood_score(mood, mood_effect)
    a_score = affinity  # 假设已经在0-1之间
    # t_score = topic_relevance  # 假设已经在0-1之间

    # 综合得分
    composite_score = (
        WEIGHTS['personality'] * p_score +
        WEIGHTS['mood'] * m_score +
        WEIGHTS['affinity'] * a_score 
        #WEIGHTS['topic_relevance'] * t_score
    )

    return composite_score >= THRESHOLD

# 示例使用
if __name__ == "__main__":
    # 示例输入
    personality = {
        'Openness': 0.7,
        'Conscientiousness': 0.6,
        'Extraversion': 0.5,
        'Agreeableness': 0.8,
        'Neuroticism': 0.3
    }

    # 每个人格特质对话题的权重（根据实际情况调整）
    topic_personality_weights = {
        'Openness': 0.9,
        'Conscientiousness': 0.6,
        'Extraversion': 0.7,
        'Agreeableness': 0.8,
        'Neuroticism': 0.4
    }

    mood = {
        'Valence': 0.8,
        'Arousal': 0.5,
        'Dominance': 0.6
    }

    # 每个VAD维度对话题的影响权重（根据实际情况调整）
    topic_mood_effect = {
        'Valence': 0.7,
        'Arousal': 0.3,
        'Dominance': 0.5
    }

    affinity = 0.75
    topic_relevance = 0.85

    should_activate = calculate_topic_activation(
        personality=personality,
        personality_weights=topic_personality_weights,
        mood=mood,
        mood_effect=topic_mood_effect,
        affinity=affinity
        # ,topic_relevance=similarity
    )

    if should_activate:
        print("激发话题: 是")
    else:
        print("激发话题: 否")
