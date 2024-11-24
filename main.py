import gen_plot
import clock
import dialogue_abstract
import favorability
import stimulate
api_key = "填自己的"
base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
def user_select_screenplay(screenplay):
    clock = clock.CallCountClock()#初始为1
    favorability = favorability.Favorability()#初始为50
    match screenplay:
        case "A screenplay":
            state_instance = gen_plot.State("A file fold path")
            #TODO：在这里选择bot
    gen_plot.generator(state_instance, base_url, api_key)



def user_chat(input):
    #TODO：在这里输入用户的对话
    return 0

mood={
    'Valence': 0.7,
    'Arousal': 0.3,
    'Dominance': 0.5
}

def next():
    clock = clock.get_time()#更新时间
    
    match favorability.get_favorability():
        case 50..59:
            user_select_screenplay.state_instance.update(1)
        case 60..69:
            user_select_screenplay.state_instance.update(2)
        case 70..79:
            user_select_screenplay.state_instance.update(3)
        case 80..89:
            user_select_screenplay.state_instance.update(4)
        case 90..99:
            user_select_screenplay.state_instance.update(5)
        case 100:
            user_select_screenplay.state_instance.update(6)
    gen_plot.generator(user_select_screenplay.state_instance, base_url, api_key)
    calculator = stimulate.TopicActivationCalculator(mood)#TODO:提供一个mood接口




