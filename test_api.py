import requests
import json

def print_json(obj):
    """格式化打印JSON对象"""
    if isinstance(obj, str):
        obj = json.loads(obj)
    
    # 打印每个字段
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "response":
                print(f"\n回复: {value}")
            elif key == "mood":
                print(f"情绪值: {value}")
                print(f"  - 情绪效价(Valence): {value[0]}")
                print(f"  - 唤醒度(Arousal): {value[1]}")
                print(f"  - 支配度(Dominance): {value[2]}")
            elif key == "favorability":
                print(f"好感度: {value}")
            elif key == "clock":
                print(f"对话次数: {value}")
            elif key == "state":
                print(f"剧情阶段: {value}")
            elif key == "message":
                print(f"消息: {value}")
    print("\n" + "="*50)

def test_api():
    # API基础URL
    base_url = "http://localhost:8000"
    
    while True:
        print("\n请选择操作：")
        print("1. 初始化游戏")
        print("2. 发送对话")
        print("3. 下一个剧情")
        print("4. 退出")
        
        choice = input("\n请输入选项（1-4）: ")
        
        if choice == "1":
            print("\n初始化游戏...")
            response = requests.post(f"{base_url}/init")
            print_json(response.json())
            
        elif choice == "2":
            message = input("\n请输入对话内容: ")
            chat_data = {"input": message}
            print("\n发送对话...")
            response = requests.post(f"{base_url}/chat", json=chat_data)
            print_json(response.json())
            
        elif choice == "3":
            print("\n获取下一个剧情...")
            response = requests.post(f"{base_url}/next")
            print_json(response.json())
            
        elif choice == "4":
            print("\n感谢使用！")
            break
        
        else:
            print("\n无效的选项，请重试")

if __name__ == "__main__":
    print("欢迎使用对话游戏API测试工具！")
    print("提示：需要先运行 python api.py 启动服务器")
    print("="*50)
    
    test_api()
