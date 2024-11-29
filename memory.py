import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    role: str  # 'user' 或 'assistant'
    content: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
class MemoryManager:
    def __init__(self, max_messages: int = 100, persistence_path: Optional[str] = None):
        self.max_messages = max_messages
        self.messages: List[Message] = []
        self.persistence_path = persistence_path
        
        # 如果指定了持久化路径，则尝试加载历史数据
        if persistence_path:
            self.load_from_file()
    
    def add_message(self, role: str, content: str) -> None:
        """添加新消息"""
        message = Message(role=role, content=content)
        self.messages.append(message)
        
        # 如果超过最大消息数，删除最早的消息
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            
        # 如果启用了持久化，则保存到文件
        if self.persistence_path:
            self.save_to_file()
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """获取历史消息，可选择只返回最后n条"""
        messages = self.messages[-last_n:] if last_n else self.messages
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    def clear(self) -> None:
        """清空所有消息"""
        self.messages.clear()
        if self.persistence_path:
            self.save_to_file()
            
    def remove_earliest_message(self) -> None:
        """删除最早的一条消息"""
        if self.messages:
            self.messages.pop(0)
            if self.persistence_path:
                self.save_to_file()
    
    def save_to_file(self) -> None:
        """将消息保存到文件"""
        if not self.persistence_path:
            return
        
        # 将消息转换为字典列表
        data = [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in self.messages
        ]
        
        # 保存到文件
        with open(self.persistence_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self) -> None:
        """从文件加载消息"""
        try:
            with open(self.persistence_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.messages = [
                    Message(
                        role=msg["role"],
                        content=msg["content"],
                        timestamp=msg["timestamp"]
                    )
                    for msg in data
                ]
        except (FileNotFoundError, json.JSONDecodeError):
            self.messages = []
