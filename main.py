import gen_plot
import clock
import dialogue_abstract
import favorability
import stimulate
from oneesan import Oneesan  # 修改导入方式
import memory
import similarity
import chardet
import os

# 全局变量
api_key = "YOUR_API_KEY"
base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"

class GameState:
    def __init__(self):
        self.state_instance = None
        self.clock_instance = None
        self.favorability_instance = None
        self.oneesan = None
        self.similarity_instance = None
        self.custom_prompts = None

game_state = GameState()

def user_select_screenplay(screenplay):

    game_state.clock_instance = clock.CallCountClock()  # 初始为1
    game_state.similarity_instance = similarity.TextSimilarity(
        api_key=api_key,
        history_dir="history"  # 指定历史记录目录
    )
    match screenplay:
        case "A screenplay":
            game_state.state_instance = gen_plot.State("history")
            game_state.oneesan = Oneesan(api_key=api_key, base_url=base_url)
    
    plot = gen_plot.generator(game_state.state_instance, base_url, api_key)
    if plot is None:
        print("生成剧情失败")
        return
    
    #第一组对话
    file_path = 'history/stage_1.txt'
    if os.path.exists(file_path):
        # 使用二进制模式读取UTF-8编码的文件
        with open(file_path, 'rb') as f:
            text = f.read().decode('utf-8')
            
        game_state.custom_prompts = text
        game_state.oneesan = Oneesan(api_key=api_key, base_url=base_url, custom_prompt={"情景": game_state.custom_prompts})
        result = game_state.oneesan.chat("详细地概括一下剧情，着重于人物的心理，情感变化以及人际关系")
        print(result["句子"])
        print(game_state.oneesan.get_mood())
        mood = game_state.oneesan.get_mood()
        print(mood)
        game_state.favorability_instance = favorability.Favorability(mood)  # 初始为50


def user_chat(input):
    game_state.clock_instance.increment()
    current_state = game_state.state_instance.get_state()
    result = game_state.oneesan.chat(input)
    print(result["句子"])
    mood = game_state.oneesan.get_mood()
    print(mood)
    game_state.favorability_instance.add_change(mood)
    if game_state.clock_instance.get_time() %10 == 0:
        abstract_text = dialogue_abstract.dialogue_abstract(
        base_url,
        api_key,
        'Oneesan/memory.txt',
        current_state
        )
        game_state.oneesan.clear_memory()  # 使用实例方法而不是类方法
        mood_dict = {
        'Valence': mood[0],
        'Arousal': mood[1],
        'Dominance': mood[2]
        }
        stimulate_calculator = stimulate.TopicActivationCalculator(mood_dict)
        should_activate = stimulate_calculator.calculate_activation()
        if should_activate:
            similar_texts = game_state.similarity_instance.find_similar_in_history(
            source_text=abstract_text,
            stage=current_state,  # 会在stage 3到stage 1的内容中查找
            top_k=1,
            threshold=0.8
            )
            if similar_texts:
                game_state.custom_prompts = game_state.custom_prompts+similar_texts





def next():
    """
    更新游戏状态并生成新的剧情
    """
    # 更新时钟
    game_state.clock_instance.increment()
    game_state.clock_instance.get_time()
    
    # 获取好感度并更新状态
    fav = game_state.favorability_instance.get_favorability()
    if 50 <= fav < 60:
        game_state.state_instance.update(1)
    elif 60 <= fav < 70:
        game_state.state_instance.update(2)
    elif 70 <= fav < 80:
        game_state.state_instance.update(3)
    elif 80 <= fav < 90:
        game_state.state_instance.update(4)
    elif 90 <= fav < 100:
        game_state.state_instance.update(5)
    elif fav >= 100:
        game_state.state_instance.update(6)
    
    # 生成新剧情
    next_scene = gen_plot.generator(game_state.state_instance, base_url, api_key)
    if game_state.state_instance.get_state()%3 == 0:
        gen_plot.generator(game_state.state_instance, base_url, api_key)
    game_state.custom_prompts = next_scene
    game_state.oneesan = Oneesan(api_key=api_key, base_url=base_url, custom_prompt={"情景": game_state.custom_prompts})
    result = game_state.oneesan.chat("详细地概括一下剧情，着重于人物的心理，情感变化以及人际关系")
    print(result)
    return result["句子"]

def test_state():
    # 初始化剧本
    user_select_screenplay("A screenplay")
    
    # 检查初始状态
    print(f"当前状态: {game_state.state_instance.get_state()}")
    print(f"时钟: {game_state.clock_instance.get_time()}")
    print(f"好感度: {game_state.favorability_instance.get_favorability()}")