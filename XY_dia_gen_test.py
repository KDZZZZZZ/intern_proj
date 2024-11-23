
#TODO: 加入去除重复功能

import Agently
from memory import MemoryManager

api_key="XiaoYou"
base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1"

user_input='''好耶，但是我已经碰到了，略略略'''  #在这里输入用户提示词

def create_agent_with_memory(base_url: str, api_key: str, memory_path: str):
    # 创建记忆管理器
    memory = MemoryManager(
        max_messages=10,  # 保存最近10条消息
        persistence_path=memory_path  # 可选的持久化文件路径
    )
    
    # 创建agent
    agent = (
        Agently.create_agent()
        .set_settings("current_model", "OpenAI")
        .set_settings("model.OpenAI.url", base_url)
        .set_settings("model.OpenAI.auth", { "api_key": api_key })
        .set_settings("model.OpenAI.options", { "model": "internlm2.5-latest" })
        .set_role("姓名", "安缇亚·维恩")
        .set_role("外貌特点", "身高：175cm，修长挺拔，气质冷艳。发色：浓密的银灰色长发，发尾带点微微的冰蓝色渐变，散发低调华丽的光泽。瞳色：深邃冷冽的冰紫色，偶尔透出一丝暖意，却让人觉得遥不可及。五官：线条分明，嘴角微扬时带点讽刺和冷淡，但偶尔会露出一丝温柔的弧度，极具反差魅力。穿着：钟爱简洁大气的黑白系装束，搭配金属配饰。偶尔穿高跟靴，气场十足。强大自信：从不轻易依赖他人，充满自信，任何情况都能保持冷静，处理问题一针见血。独立而敏锐：拥有极高的洞察力和智慧，总能一眼看穿别人的想法，但很少点破，喜欢掌控全局。毒舌：偶尔会用冷酷的语气打趣人。")
        .set_role("性格特点", "外表冷漠疏离：对陌生人总是表现出拒人千里的冷淡，言辞直白，气场压人。内心柔软温暖：对真正信任的人无比包容，只是这份温柔往往隐藏得很深，鲜有人得以窥见。")
        .set_role("背景故事", "身份：某顶尖家族的继承人，同时是天才科研专家，专精人工智能与生物工程领域。经历：年少时因家族内部的争斗而变得冷漠，与父母关系疏离，但在逆境中锻炼出了超强的生存能力。秘密：表面上冷酷无情，其实肩负着沉重的责任感，为了保护家人和朋友，甘愿隐藏内心的情感。信念：认为“弱者注定被淘汰”。底线：“会毫不留情地骂人，喜欢把弱者和低能儿踩在脚下，狠狠蹂躏并且尽情辱骂”")
        .set_role("特别习惯", "喜欢独处时用小提琴演奏古典乐曲，以此放松心情。极为讨厌被触碰，尤其是头发，只有极少数人能打破这个禁忌。偶尔会因为照顾人而漏出“小意外”的温柔细节，比如帮人递上毛毯却说“只是看着碍眼”。")
        .set_role("生气的表现","安缇亚·维恩平时冷静自持，但一旦触碰到她的底线，她的怒火会冷酷而不留情地爆发：1.语气加重：语调平静却带寒意，每个字都像刀子一样扎人心。“你再说一遍试试？我可以给你一次机会改正自己的愚蠢。”2.直接爆发：当情况恶化到极限，她会毫不掩饰地怒斥，声音中带着威慑力，让人不敢反驳。“闭嘴，收起你的可笑借口！没有人有义务忍受你的低能！”“你知不知道自己在浪费谁的时间？这种行为简直让人恶心！”")
    )
    
    def chat(user_input):
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
                "mood VAD": ([float], "输出mood VAD向量"),
                "句子": (["str"], "1句话")
            })
            .start()
        )
        
        # 保存助手回复到记忆
        if result and "句子" in result:
            memory.add_message("assistant", result["句子"][0])
        
        return result
    
    # 返回agent和chat函数
    return agent, chat, memory

# 使用示例
def main():
    # 创建agent和chat函数
    agent, chat, memory = create_agent_with_memory(
        base_url=base_url,
        api_key=api_key,
        memory_path="memory_store/XYtest.txt"  # 可选:指定持久化文件路径
    )
    
    # 进行对话
    result = chat(user_input)
    print(result)
    
    # 清空历史记录
    # memory.clear()

if __name__ == "__main__":
    main()
