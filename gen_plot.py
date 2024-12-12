import Agently
import numpy as np
import chardet
import os
import history
prompt = """- Role: 情节构建专家和对话创作大师
- Background: 用户拥有一个小说的前面部分，需要续写情节来丰富故事内容，特别是需要一段两人之间的交流情节来增强故事的深度和人物之间的关系。可以有挫折和磨难的部分。
- Profile: 你是一位经验丰富的情节构建专家和对话创作大师，擅长通过对话来展现人物性格，推动情节发展，并增强读者的沉浸感。
- Skills: 你具备深厚的文学素养和对话创作技巧，能够根据小说的情节大纲设计出既符合逻辑又引人入胜的对话场景。
- Goals: 创作一段两人之间的交流情节，通过对话展现人物性格，加深人物关系，同时推动故事情节的发展。
- Constrains: 对话需要符合小说的整体风格和情节设定，人物语言要符合其性格特征，情节要与已有部分保持一致，不得出现与前面内容相悖的内容。
- OutputFormat: 对话文本，包含人物动作和表情描述，以及符合情境的对话内容。
- Workflow:
  1. 确定对话中涉及的人物及其性格特点。
  2. 根据情节大纲确定对话的主题和目的。
  3. 设计对话内容，确保对话自然流畅，能够展现人物性格和推动情节发展。
  4. 检查对话是否符合小说风格和情节设定，进行必要的调整。
- Examples:
  - 例子1：两个角色在紧张的逃亡中偶遇，对话中透露出他们对彼此的信任和依赖。
  - 例子2：角色A向角色B透露一个重大秘密，对话中展现角色A的犹豫和角色B的震惊。
  - 例子3：两个角色在庆祝胜利时的轻松对话，展现他们之间的友情和对未来的期待。
"""




# 定义State类
class State:
    def __init__(self, directory):
        self.directory = directory
        self.state = self._get_initial_state()
    
    def _get_initial_state(self):
        # 获取目录中已存在的状态文件，确定初始状态号
        files = [f for f in os.listdir(self.directory) if f.startswith('state_') and f.endswith('.txt')]
        if not files:
            return 1
        states = [int(f.split('_')[1].split('.')[0]) for f in files]
        return max(states) + 1
    
    def update(self,new_state):
        # 增加状态数
        self.state = new_state
    
    def get_state(self):
        # 获取当前状态数
        return self.state
    
    def state_list(self):
        # 生成状态列表
        return np.arange(1, self.state + 1)

# 处理状态文件并生成代理输出的主函数
def generator(state_instance, base_url, api_key, prompt=prompt):
    """
    处理状态文件并生成代理输出。

    参数:
    - state_instance (State): 状态管理实例。
    - base_url (str): 代理API的基础URL。
    - api_key (str): 认证用的API密钥。
    - prompt (str): 引导代理处理的提示。

    返回:
    - str: 代理的输出。
    """
    try:
        # 获取当前状态数
        n = state_instance.get_state()
        
        # 生成文件列表
        file_list = [os.path.join(state_instance.directory, f'stage_{i}.txt') for i in state_instance.state_list()]
        
        # 收集所有状态文件的内容
        collected_text = ''
        for file_path in file_list:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    if raw_data:
                        result = chardet.detect(raw_data)
                        encoding = result['encoding'] if result['encoding'] else 'utf-8'
                        text = raw_data.decode(encoding)
                        collected_text += text + '\n'  # 文件间加换行符
        
        agent = (
            Agently.create_agent()
            .set_settings("current_model", "OpenAI")
            .set_settings("model.OpenAI.url", base_url)
            .set_settings("model.OpenAI.auth", {"api_key": api_key})
            .set_settings("model.OpenAI.options", {"model": "internlm2.5-latest"})
        )
        
        # 传递收集的文本给代理并获取输出
        result = (
            agent
            .instruct(prompt)
            .input(collected_text)
            .output({
                "句子": (str,"生成下一个连贯的情景，一句话概括")
            })
            .start()
        )
        
        if result is None or '句子' not in result:
            print("生成对话失败")
            return None
            
        # 获取代理的输出
        agent_output = result['句子']
        
        # 将代理的输出写入state_n_agent.txt文件
        output_file_path = os.path.join(state_instance.directory, f'stage_{n}.txt')
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # 写入新内容
        with open(output_file_path, 'a', encoding='utf-8') as f:
            f.write('\n' + agent_output)
            
        # 生成文件哈希
        file_hash = history.generate_hash(output_file_path)
        if file_hash is not None:
            history.global_files[output_file_path] = file_hash
            print(f"文件 {output_file_path} 已添加到全局字典中。")
        else:
            print(f"无法生成文件 {output_file_path} 的哈希值。")
        
        print(f"代理的输出已保存到 {output_file_path}")
        return agent_output
    
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

# 示例用法
if __name__ == '__main__':
    # 用户创建State实例并管理状态
    state_dir = 'history'
    state_instance = State(directory=state_dir)
    
    base_url = 'https://api.openai.com/v1'
    api_key = ""
        
    # 调用process_states函数处理状态文件
    output = generator(state_instance, base_url, api_key)
    if output:
        print("处理完成。输出已保存。")
    
    # 用户在需要时增加状态数
    # state_instance.add_1()    # 调用process_states函数处理状态文件
    output = generator(state_instance, base_url, api_key, prompt)
    if output:
        print("处理完成。输出已保存。")
    
    # 用户在需要时增加状态数
    # state_instance.add_1()