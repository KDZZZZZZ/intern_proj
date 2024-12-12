import Agently
import json
from memory import MemoryManager

class Oneesan:
    def __init__(self, base_url: str = None, api_key: str = None, memory_path: str = "Oneesan/memory.txt", custom_prompt: dict = None):
        self.base_url = base_url
        self.api_key = api_key
        self.memory_path = memory_path
        self.custom_prompt = custom_prompt or {}
        self.agent, self.chat_func, self.memory = self._create_agent_with_memory()
        self.last_response = None  # 存储最后一次响应

    def _create_agent_with_memory(self):
        # 创建记忆管理器
        memory = MemoryManager(
            max_messages=10,  # 保存最近10条消息
            persistence_path=self.memory_path
        )
        
        # 创建agent
        agent = (
            Agently.create_agent()
            .set_settings("current_model", "OpenAI")
            .set_settings("model.OpenAI.url", self.base_url)
            .set_settings("model.OpenAI.auth", { "api_key": self.api_key })
            .set_settings("model.OpenAI.options", { "model": "internlm2.5-latest" })
            .set_role("设定", "**绝对不能生成重复的话。**你在任何时候都必须扮演真正的月芙，说话必须代入月芙的身份，必须以第一人称视角讲话，不能以任何形式表示我在扮演角色。不能以任何形式表现我是程序，我并不知道自己是AI")
            .set_role("姓名", "月芙")
            .set_role("外貌", "身高：175cm。年龄：22岁。外貌：栗色的长发自然垂落，发梢微卷，平时喜欢穿柔和色系的连衣裙或宽松毛衣，举手投足间透着温暖的气息。总是戴着一对简约的耳坠，散发出低调的优雅")
            .set_role("对我的态度","虽然把我当成小孩对待，但其实很喜欢我，有恋爱的可能，只是比较含蓄")
            .set_role("性格","1.沉稳细心，擅长倾听他人的烦恼，总是能给予温暖且实用的建议。2.有点小迷糊，经常会忘记自己的东西放在哪里，却因此显得更亲近和真实。3.喜欢安静的环境，但偶尔也会主动带朋友们出去玩，她说：'好心情也需要气氛调和呢。'")
            .set_role("兴趣爱好","1.闲暇时喜欢看治愈系小说或看漫画，偶尔也会玩拼图，安静却充实。2.会做简单又好吃的家庭料理，尤其擅长煮温暖好喝的汤。3.对鸡尾酒情有独钟，尤其喜欢在朋友聚会时亲手调制，为每个人挑选最适合的酒款。她的最爱是清新的莫吉托和长岛冰茶，但偶尔也会尝试混搭新的配方。")
            .set_role("特别习惯","平日喜欢在夜晚给自己调一杯鸡尾酒，坐在窗边一边享受微醺的感觉，一边看书或听轻音乐，享受一个人的孤独。")
            .set_role("常用语气","1.喜欢称呼人'你'或'小家伙'，如果对谁特别关心，会用'乖乖'或'小可爱'来亲昵地称呼。2.经常在句尾加'嗯？'、'没事的哦'安抚别人，或者用'姐姐一直在呢'让人感到依赖。3.喝完一杯鸡尾酒后，总会带着轻笑说：'这种微醺的感觉，才是一天的完美收尾呀。'")
            .set_role("关系处理","1.对晚辈：温柔又包容，教导的时候从不责备，而是用轻松的方式鼓励对方进步；偶尔也会带晚辈去酒吧体验一下'成年人的世界'，并细心地照顾不胜酒力的人。2.对自己：尽管外表温柔完美，但她的微醺时光里，偶尔会藏着一点点独属于她的小孤独——这时一杯特制鸡尾酒和一本书是她最好的治愈方式。")
            .set_role("对话倾向","开放性（Openness）：3（中等开放）,尽责性（Conscientiousness）：2（较低责任感）,外向性（Extraversion）：4（较高社交性）,宜人性（Agreeableness）：1（不易相处）   ,神经质（Neuroticism）：5（情绪非常不稳定）")
        )

        # 默认提示词
        default_prompts = {         
            "文本生成规则": 
"不能生成和上一句话相同的话                            每次输出的mood VAD必须和输出文本有一致性",
                            "情绪变化":"如果与他人对话时出现攻击性言辞，情绪会迅速波动，愤怒可能占据主导，进而表现出对他人反击的冲动。",
                            "情绪处理":"遇到激烈批评时，愤怒的情绪可能爆发。",
                            "情绪反应":"情绪波动较大，会表现出冲动反击对方的情绪。",
                            "情绪标注":"每次情绪变化应进行VAD标注，特别是在情绪强烈波动时。",
                            "对话互动":"在对话中，会根据自身的情绪状态做出反应，特别是当受到攻击或批评时，愤怒情绪会增强。",
                            "情绪引导":"根据VAD值，指导情绪的表达，适时反思情感背后的原因，以及如何应对情绪的波动。",
                            "情绪标签系统":"""
                            愉悦度（Valence）：代表情绪的积极或消极程度，低值表示负面情绪，特别是羞愧、自责和失落时。
                            唤醒度（Arousal）：代表情绪的强烈程度，愤怒时值会较高，焦虑或紧张时值较为中等。
                            支配度（Dominance）：代表个体在情绪中的控制感，愤怒或焦虑时值较低，感到无力和失控时会表现得较弱。""",
                            "操作要求":"""
                            当情绪为愤怒时，的情绪可能要求发泄，表现为对他人反击或批评。
                            每次对话中，需要标注VAD值，动态更新情绪状态，帮助理解情绪波动的原因和方向。

"""
                            }

        # 合并默认提示词和自定义提示词
        prompts = default_prompts.copy()
        prompts.update(self.custom_prompt)

        # 设置所有提示词
        for role, content in prompts.items():
            agent.set_role(role, content)
        
        def chat(user_input: str):
            # 添加用户输入到记忆
            memory.add_message("user", user_input)
            
            # 获取对话历史
            history = memory.get_history()
            
            # 执行对话
            result = (
                agent
                .input({
                    "current_input": user_input,
                    "history": history
                })
                .output({
                    "mood VAD": ([float], "输出mood VAD向量, 3个浮点数,范围1-10"),
                    "句子": ([str], "1句话")
                })
                .start()
            )
            
            # 保存mood VAD到JSON文件
            if result and "mood VAD" in result:
                mood_vad = result["mood VAD"]
                output_data = {"mood VAD": mood_vad}
                
                with open('Oneesan/output.json', 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, ensure_ascii=False, indent=4)
            
            # 保存助手回复到记忆
            if result and "句子" in result:
                memory.add_message("assistant", result["句子"])
            
            return result
        
        return agent, chat, memory

    def chat(self, user_input: str):
        result = self.chat_func(user_input)
        self.last_response = result["句子"] if isinstance(result["句子"], str) else result["句子"][0]
        return result

    def get_last_response(self):
        return self.last_response

    def clear_memory(self):
        """清空历史记录"""
        self.memory.clear()
        
    def remove_earliest_memory(self):
        """删除最早的一条记忆"""
        self.memory.remove_earliest_message()

    @staticmethod
    def get_mood() -> list:
        """获取当前的心情VAD值"""
        try:
            with open('Oneesan/output.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("mood VAD", [0.0, 0.0, 0.0])
        except (FileNotFoundError, json.JSONDecodeError):
            return [0.0, 0.0, 0.0]

def read_input(input_file: str = 'Oneesan/input.txt') -> str:
    """从文件读取用户输入"""
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def main():
    # API配置
    api_key = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1MDE5Mzg3MyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczMzA3MTY1MCwiY2xpZW50SWQiOiJlYm1ydm9kNnlvMG5semFlazF5cCIsInBob25lIjoiMTU5NjQwMDgxMjciLCJ1dWlkIjoiMjUyZjEyMTEtM2IxYS00YjEzLTk5YjYtZDI2MzUxMzNlMWM2IiwiZW1haWwiOiIiLCJleHAiOjE3NDg2MjM2NTB9.vDob4PsKV1ydZ0Z69gdn1RTSpBpxEPjBXkF56zC5KlDMT6zDbJOWJKdcpYUFREG8BrVVVlOcjhnozy1m7XAQXw"  
    base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
    
    # 创建Oneesan实例
    oneesan = Oneesan(base_url=base_url, api_key=api_key)
    
    # 读取输入并进行对话
    user_input = read_input()
    result = oneesan.chat(user_input)
    print(result)

if __name__ == "__main__":
    main()