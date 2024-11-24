import numpy as np
from typing import Dict, Union
personality = {
    'Openness': 0.7,
    'Conscientiousness': 0.6,
    'Extraversion': 0.5,
    'Agreeableness': 0.8,
    'Neuroticism': 0.3
}
    
topic_personality_weights = {
    'Openness': 0.9,
    'Conscientiousness': 0.6,
    'Extraversion': 0.7,
    'Agreeableness': 0.8,
    'Neuroticism': 0.4
}



topic_mood_effect = {
    'Valence': 0.7,
    'Arousal': 0.3,
    'Dominance': 0.5
}

affinity = 0.75
class TopicActivationCalculator:
    """计算话题激活的类"""
    
    # 默认权重配置
    DEFAULT_WEIGHTS = {
        'personality': 0.3,
        'mood': 0.2, 
        'affinity': 0.3,
        'topic_relevance': 0.2
    }
    
    # 默认阈值
    DEFAULT_THRESHOLD = 0.6

    def __init__(
        self, mood,
        personality = personality,
        personality_weights = topic_personality_weights,
       
        mood_effect = topic_mood_effect,
        affinity = affinity,
        weights: Dict[str, float] = None,
        threshold: float = None
    ):
        """
        初始化话题激活计算器
        
        Args:
            personality: 人格特质分数字典
            personality_weights: 人格特质权重字典
            mood: VAD情感状态分数字典
            mood_effect: VAD影响权重字典
            affinity: 好感度分数(0-1)
            weights: 可选的自定义权重配置
            threshold: 可选的自定义阈值
        """
        self.personality = personality
        self.personality_weights = personality_weights
        self.mood = mood
        self.mood_effect = mood_effect
        self.affinity = affinity
        
        self.weights = weights if weights is not None else self.DEFAULT_WEIGHTS
        self.threshold = threshold if threshold is not None else self.DEFAULT_THRESHOLD
        
        self._validate_inputs()

    def _validate_inputs(self):
        """验证输入参数的有效性"""
        if not 0 <= self.affinity <= 1:
            raise ValueError("Affinity must be between 0 and 1")
        
        # 可以添加更多验证...

    @staticmethod
    def normalize(vector: np.ndarray) -> np.ndarray:
        """标准化向量到0-1范围"""
        min_val = np.min(vector)
        max_val = np.max(vector)
        if max_val - min_val == 0:
            return np.zeros_like(vector)
        return (vector - min_val) / (max_val - min_val)

    def _personality_score(self) -> float:
        """计算人格特质评分"""
        score = 0
        for trait in self.personality:
            score += self.personality[trait] * self.personality_weights.get(trait, 0)
        return self.normalize(np.array([score]))[0]

    def _mood_score(self) -> float:
        """计算情感状态评分"""
        score = 0
        for dim in self.mood:
            score += self.mood[dim] * self.mood_effect.get(dim, 0)
        return self.normalize(np.array([score]))[0]

    def calculate_activation(self) -> bool:
        """
        计算是否应该激活话题
        
        Returns:
            bool: 是否激活话题
        """
        p_score = self._personality_score()
        m_score = self._mood_score()
        
        composite_score = (
            self.weights['personality'] * p_score +
            self.weights['mood'] * m_score +
            self.weights['affinity'] * self.affinity
        )
        
        return composite_score >= self.threshold

    def update_personality(self, personality: Dict[str, float]):
        """更新人格特质"""
        self.personality = personality
        
    def update_mood(self, mood: Dict[str, float]):
        """更新情感状态"""
        self.mood = mood
        
    def update_affinity(self, affinity: float):
        """更新好感度"""
        if not 0 <= affinity <= 1:
            raise ValueError("Affinity must be between 0 and 1")
        self.affinity = affinity

# 使用示例
if __name__ == "__main__":
    personality = {
        'Openness': 0.7,
        'Conscientiousness': 0.6,
        'Extraversion': 0.5,
        'Agreeableness': 0.8,
        'Neuroticism': 0.3
    }
    
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
    
    topic_mood_effect = {
        'Valence': 0.7,
        'Arousal': 0.3,
        'Dominance': 0.5
    }
    
    affinity = 0.75
    
    calculator = TopicActivationCalculator(
        personality=personality,
        personality_weights=topic_personality_weights,
        mood=mood,
        mood_effect=topic_mood_effect,
        affinity=affinity
    )
    
    should_activate = calculator.calculate_activation()
    print(f"激发话题: {'是' if should_activate else '否'}")
