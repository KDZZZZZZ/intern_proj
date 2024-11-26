import math

class Favorability:
    def __init__(self, moodvads):
        self.moodvads = [(moodvads[0], moodvads[1], moodvads[2])]
        self.favorability = 50  # 初始好感度保持在50
        self.history_weights = []  # 用于平滑处理的权重

    def add_change(self, moodvad):
        """添加新的情绪变化 (V, A, D)"""
        self.moodvads.append(moodvad)
        # 限制历史记录长度，防止过长影响性能
        if len(self.moodvads) > 50:
            self.moodvads.pop(0)

    def calculate_trend(self):
        """计算情绪趋势并进行平滑"""
        trend = 0
        weight_sum = 0
        self.history_weights = [
            math.exp(-0.1 * i) for i in range(len(self.moodvads))
        ]  # 指数平滑权重
        self.history_weights.reverse()  # 越近期的情绪权重越高
        
        for i, (v, _, _) in enumerate(self.moodvads):
            trend += v * self.history_weights[i]
            weight_sum += self.history_weights[i]
        return trend / weight_sum if weight_sum != 0 else 0

    def get_favorability(self):
        """根据情绪变化记录计算稳定的好感度"""
        trend = self.calculate_trend()  # 平滑后的情绪趋势
        delta = trend - 5  # 假设 5 为中性情绪
        stability_factor = 0.2  # 降低好感度变化幅度
        self.favorability += delta * stability_factor

        # 高好感度时的衰减机制
        if self.favorability > 75:
            self.favorability -= (self.favorability - 75) * 0.1

        # 低好感度时的修复机制
        if self.favorability < 25:
            self.favorability += (25 - self.favorability) * 0.1

        # 限制好感度范围
        self.favorability = max(0, min(100, self.favorability))
        return self.favorability


# 示例使用