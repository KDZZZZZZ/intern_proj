from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import main
from typing import Dict, Any
from fastapi.responses import JSONResponse
import json

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
        
        # 使用JSONResponse并确保正确的编码
        return JSONResponse(content={
            "response": main.game_state.oneesan.get_last_response(),
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }, media_type="application/json; charset=utf-8")
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
        
        return JSONResponse(content={
            "response": response,
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }, media_type="application/json; charset=utf-8")
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
        main.api_key = ""
        main.base_url = "https://internlm-chat.intern-ai.org.cn/puyu/api/v1"
        
        # 选择剧本并初始化
        main.user_select_screenplay("A screenplay")
        
        # 获取所有状态信息
        response = main.game_state.oneesan.chat("")["句子"]  # 获取初始对话
        mood = main.game_state.oneesan.get_mood()
        favorability = main.game_state.favorability_instance.get_favorability()
        clock = main.game_state.clock_instance.get_time()
        state = main.game_state.state_instance.get_state()
        
        return JSONResponse(content={
            "message": "Game initialized successfully",
            "response": response,
            "mood": mood,
            "favorability": favorability,
            "clock": clock,
            "state": state
        }, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
