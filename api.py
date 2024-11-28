from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import main
from typing import Dict, Any
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime

app = FastAPI(title="Game API", description="API for game interactions")

class ScreenplayRequest(BaseModel):
    screenplay: str

class ChatRequest(BaseModel):
    input: str

class ApiKeyRequest(BaseModel):
    api_key: str
    base_url: str = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"

class InitRequest(BaseModel):
    api_key: str
    base_url: str = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"

def save_response_to_file(endpoint: str, response_data: Dict[str, Any]):
    """保存 API 响应到单个JSON文件，每次都覆盖之前的内容"""
    filename = "responses.json"
    
    # 验证响应数据是否可以被序列化为JSON
    try:
        # 先尝试序列化响应数据，确保它是有效的JSON
        json.dumps(response_data, ensure_ascii=False)
    except (TypeError, json.JSONDecodeError) as e:
        print(f"Error: Invalid response data format: {str(e)}")
        return
    
    # 创建新的响应数据结构
    all_responses = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 设置新的响应数据
    all_responses[endpoint] = {
        timestamp: response_data
    }
    
    # 直接写入新文件，覆盖旧内容
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_responses, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error: Failed to save response data: {str(e)}")

@app.post("/select-screenplay")
@app.get("/select-screenplay/{screenplay}")
async def select_screenplay(screenplay: str = None, request: ScreenplayRequest = None):
    try:
        # Handle both GET and POST methods
        screenplay_value = screenplay if screenplay else request.screenplay if request else None
        if not screenplay_value:
            raise HTTPException(status_code=400, detail="Screenplay value is required")
        main.user_select_screenplay(screenplay_value)
        return JSONResponse(content={"message": "Screenplay selected successfully"}, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
@app.get("/chat/{input}")
async def chat(input: str = None, request: ChatRequest = None):
    try:
        # Handle both GET and POST methods
        chat_input = input if input else request.input if request else None
        if not chat_input:
            raise HTTPException(status_code=400, detail="Chat input is required")
        
        # 进行对话
        main.user_chat(chat_input)
        
        # 获取最新的状态信息
        mood = main.game_state.oneesan.get_mood()
        favorability = main.game_state.favorability_instance.get_favorability()
        clock = main.game_state.clock_instance.get_time()
        state = main.game_state.state_instance.get_state()
        
        # 准备响应数据
        response_data = {
            "response": main.game_state.oneesan.get_last_response(),
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }
        
        # 保存响应到文件
        save_response_to_file("chat", response_data)
        
        # 返回响应
        return JSONResponse(content=response_data, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/next")
@app.get("/next")
async def next_plot():
    try:
        response = main.next()
        
        # 获取所有状态信息
        mood = main.game_state.oneesan.get_mood()
        favorability = main.game_state.favorability_instance.get_favorability()
        clock = main.game_state.clock_instance.get_time()
        state = main.game_state.state_instance.get_state()
        
        # 准备响应数据
        response_data = {
            "response": response,
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }
        
        # 保存响应到文件
        save_response_to_file("next", response_data)
        
        return JSONResponse(content=response_data, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set-api-key")
async def set_api_key(request: ApiKeyRequest):
    try:
        main.api_key = request.api_key
        main.base_url = request.base_url
        return JSONResponse(content={"message": "API key and base URL set successfully"}, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/init")
async def initialize():
    try:
        # 设置API密钥和base_url（使用测试中的值）
        main.api_key = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiI1MDE5Mzg3MyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczMjUzNTA0OSwiY2xpZW50SWQiOiJlYm1ydm9kNnlvMG5semFlazF5cCIsInBob25lIjoiMTU5NjQwMDgxMjciLCJ1dWlkIjoiM2UxY2Y5MmUtOTA4NC00ZDI0LWI5MWEtZGI2NjlmY2M1NWM3IiwiZW1haWwiOiIiLCJleHAiOjE3NDgwODcwNDl9.YcS6spF3Qy7DcgNEAMWulOPNKIlhSTJtylCNv3hJUoaXYem-BTpk10qm6bKXor7Orb1iV3esfeuwcCL7535tzg"
        main.base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
        
        # 选择剧本并初始化
        main.user_select_screenplay("A screenplay")
        
        # 获取所有状态信息
        response = main.game_state.oneesan.chat("")["句子"]  # 获取初始对话
        mood = main.game_state.oneesan.get_mood()
        favorability = main.game_state.favorability_instance.get_favorability()
        clock = main.game_state.clock_instance.get_time()
        state = main.game_state.state_instance.get_state()
        
        # 准备响应数据
        response_data = {
            "message": "Game initialized successfully",
            "response": response,
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }
        
        # 保存响应到文件
        save_response_to_file("init", response_data)
        
        return JSONResponse(content=response_data, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
