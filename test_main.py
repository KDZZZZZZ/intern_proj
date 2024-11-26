import unittest
from unittest.mock import patch, MagicMock
import main
import os
import json
import time

class TestGameSystem(unittest.TestCase):
    def setUp(self):
        """每个测试用例前的初始化"""
        main.game_state = main.GameState()
        time.sleep(2)  # 初始化后睡眠
        
    def tearDown(self):
        """每个测试用例后的清理，添加延时避免请求过快"""
        time.sleep(3)  # 测试用例之间更长的睡眠
        
    def test_user_select_screenplay(self):
        """测试剧本选择功能"""
        print("\n=== 测试剧本选择 ===")
        time.sleep(2)  # 测试开始前睡眠
        
        # 测试选择剧本A
        main.user_select_screenplay("A screenplay")
        time.sleep(3)  # 剧本选择后睡眠
        
        print(f"选择剧本A后的状态:")
        print(f"- state_instance存在: {main.game_state.state_instance is not None}")
        time.sleep(1)  # 打印后睡眠
        
        print(f"- clock_instance存在: {main.game_state.clock_instance is not None}")
        time.sleep(1)
        
        print(f"- oneesan存在: {main.game_state.oneesan is not None}")
        time.sleep(1)
        
        print(f"- similarity_instance存在: {main.game_state.similarity_instance is not None}")
        time.sleep(1)
        
        self.assertIsNotNone(main.game_state.state_instance)
        self.assertIsNotNone(main.game_state.clock_instance)
        self.assertIsNotNone(main.game_state.oneesan)
        self.assertIsNotNone(main.game_state.similarity_instance)
        time.sleep(2)  # 断言检查后睡眠
        
        # 验证时钟初始值
        print(f"- 初始时钟值: {main.game_state.clock_instance.get_time()}")
        time.sleep(2)
        self.assertEqual(main.game_state.clock_instance.get_time(), 1)
        time.sleep(2)
        
        # 验证好感度初始值
        if main.game_state.favorability_instance:
            print(f"- 初始好感度: {main.game_state.favorability_instance.get_favorability()}")
            time.sleep(2)
            self.assertEqual(main.game_state.favorability_instance.get_favorability(), 50)
            time.sleep(2)

    def test_user_chat(self):
        """测试用户对话功能"""
        print("\n=== 测试用户对话 ===")
        time.sleep(2)  # 测试开始前睡眠
        
        # 首先需要选择剧本
        main.user_select_screenplay("A screenplay")
        time.sleep(3)  # 剧本选择后睡眠
        
        # 测试普通对话
        print("\n测试普通对话:")
        time.sleep(2)
        test_inputs = ["你好", "今天天气真好", "我们来聊聊天吧"]
        for input_text in test_inputs:
            print(f"\n输入: {input_text}")
            time.sleep(1)
            main.user_chat(input_text)
            time.sleep(3)  # 对话后睡眠
            print(f"- 当前时钟: {main.game_state.clock_instance.get_time()}")
            time.sleep(1)
            print(f"- 当前好感度: {main.game_state.favorability_instance.get_favorability()}")
            time.sleep(1)
            print(f"- 当前心情: {main.game_state.oneesan.get_mood()}")
            time.sleep(2)
        
        # 测试第10次对话时的特殊处理
        print("\n测试第10次对话:")
        time.sleep(2)
        while main.game_state.clock_instance.get_time() < 9:
            main.user_chat("继续对话")
            time.sleep(3)  # 每次对话后睡眠
            print(f"- 当前时钟: {main.game_state.clock_instance.get_time()}")
            time.sleep(1)
        main.user_chat("第10次对话")
        time.sleep(3)  # 最后一次对话后睡眠
        print(f"- 第10次对话后的时钟: {main.game_state.clock_instance.get_time()}")
        time.sleep(2)

    def test_next_function(self):
        """测试next功能和状态转换"""
        print("\n=== 测试next功能 ===")
        time.sleep(2)  # 测试开始前睡眠
        
        main.user_select_screenplay("A screenplay")
        time.sleep(3)  # 剧本选择后睡眠
        
        # 测试不同好感度区间的状态转换
        favorability_ranges = [
            (50, "初始状态"),
            (55, "50-60区间"),
            (65, "60-70区间"),
            (75, "70-80区间"),
            (85, "80-90区间"),
            (95, "90-100区间"),
            (105, "100以上")
        ]
        
        for fav, desc in favorability_ranges:
            print(f"\n测试{desc}（好感度={fav}）:")
            time.sleep(1)
            main.game_state.favorability_instance._favorability = fav
            time.sleep(1)
            main.next()
            time.sleep(3)  # next操作后睡眠
            print(f"- 当前状态: {main.game_state.state_instance.get_state()}")
            time.sleep(1)
            print(f"- 当前好感度: {main.game_state.favorability_instance.get_favorability()}")
            time.sleep(1)
            print(f"- 当前时钟: {main.game_state.clock_instance.get_time()}")
            time.sleep(2)

    def test_stimulate_trigger(self):
        """测试刺激触发机制"""
        print("\n=== 测试刺激触发机制 ===")
        main.user_select_screenplay("A screenplay")
        time.sleep(5)  # 增加剧本选择后的睡眠时间
        
        # 设置一个可能触发刺激的心情状态
        test_moods = [
            ([8, 8, 8], "高唤醒状态"),
            ([2, 2, 2], "低唤醒状态"),
            ([5, 5, 5], "中等状态")
        ]
        
        for mood, desc in test_moods:
            print(f"\n测试{desc}:")
            time.sleep(3)  # 增加每个测试状态前的睡眠时间
            result = main.game_state.oneesan.chat("你好")
            print(result["句子"])
            time.sleep(2)  # 增加聊天后的睡眠时间
            
            # 设置心情
            main.game_state.oneesan.set_mood(mood)
            time.sleep(2)  # 增加设置心情后的睡眠时间
            
            # 测试刺激触发
            result = main.game_state.oneesan.stimulate()
            if result:
                print(result["句子"])
            time.sleep(3)  # 增加刺激触发后的睡眠时间

if __name__ == '__main__':
    unittest.main(verbosity=2)
