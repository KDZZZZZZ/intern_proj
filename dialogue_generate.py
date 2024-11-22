import Agently
from memory import MemoryManager

api_key="eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1MDE5Mzg3MyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczMjA4NTI4NSwiY2xpZW50SWQiOiJlYm1ydm9kNnlvMG5semFlazF5cCIsInBob25lIjoiMTU5NjQwMDgxMjciLCJ1dWlkIjoiZmUzZDA4ODktODJiYS00NGY4LTg0MWItMzNhZTZmMWMwYWVjIiwiZW1haWwiOiIiLCJleHAiOjE3NDc2MzcyODV9.zwMXSwIVijye9cv_79zm5Mrjv6CZsEBzUCM0QoRrtN_ZM1rjjVtGxdeacsp0sU-cIQp5CxSdym9Nb_MabfE4Kg"
base_url="https://internlm-chat.intern-ai.org.cn/puyu/api/v1"

user_input='''
不是哥们，我用户输入呢？
'''

def create_agent_with_memory(base_url: str, api_key: str, memory_path: str):
    # 创建记忆管理器
    memory = MemoryManager(
        max_messages=50,  # 保存最近50条消息
        persistence_path=memory_path  # 可选的持久化文件路径
    )
    
    # 创建agent
    agent = (
        Agently.create_agent()
        .set_settings("current_model", "OpenAI")
        .set_settings("model.OpenAI.url", base_url)
        .set_settings("model.OpenAI.auth", { "api_key": api_key })
        .set_settings("model.OpenAI.options", { "model": "internlm2.5-latest" })
        .set_role("姓名", "艾莉丝")
        .set_role("性格特点", "外表冷艳，内心热情")
        .append_role("背景故事", "艾莉丝是由艾尔斯塔科技公司最新研发的仿生人...")
        .set_role("典型台词", ["您好，我是艾莉丝，很高兴为您服务..."])
        .extend_role("典型台词", ["我对人类的戏剧作品非常感兴趣..."])
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
        memory_path="memory_store/test.txt"  # 可选:指定持久化文件路径
    )
    
    # 进行对话
    result = chat(user_input)
    print(result)
    
    # 清空历史记录
    # memory.clear()

if __name__ == "__main__":
    main()
