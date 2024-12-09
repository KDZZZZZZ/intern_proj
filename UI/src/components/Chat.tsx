import React, { useEffect, useState, useRef } from 'react';
import './Chat.css';
import { useQuery } from '@tanstack/react-query';
interface Message {
    text: string;
    sender: 'user' | 'bot'; // 区分发送者
    timestamp: number; // 添加时间戳
}

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState<string>('');
    const contentRef = useRef<HTMLDivElement>(null);
    const isLoaded = useRef(false);
    const fetchData = async () => {
        const response = await fetch('http://localhost:5000/chat'); // 将'/your-api-endpoint' 替换为你的API端点
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      };
        const { data} = useQuery(
          {
           queryKey:['init'], 
           queryFn:fetchData,
          },
          );
          console.log(data);
    const sendMessage = async (message: string) => {
        try {
            const newMessage: Message = {
                text: message,
                sender: 'user',
                timestamp: Date.now(),
            };

            setMessages([...messages, newMessage]);
            setInputText('');

            const response = await fetch(`http://127.0.0.1:8000/chat?input=${encodeURIComponent(message)}`,{  method: "POST"});
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            // 更新 messages 状态，包含服务器返回的新消息
            setMessages(prevMessages => [...prevMessages, ...data.message_list.map((msg: any) => ({
                text: msg.message_text,
            }))]);

        } catch (error) {
            console.error('发送消息失败:', error);
            // 错误处理，例如将消息标记为发送失败
        }
    };


    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/chat?input=${encodeURIComponent(inputText)}`,{  method: "POST"});
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setMessages(data.message_list);
            } catch (error) {
                console.error('获取消息失败:', error);
            }
        };

        if (!isLoaded.current) {
            isLoaded.current = true;
            fetchMessages();
        }
    }, [messages]);

    useEffect(() => {
        if (contentRef.current) {
            contentRef.current.scrollTop = contentRef.current.scrollHeight;
        }
    }, [messages]);
    const send = () => {
        if (!inputText) {
            alert('请输入内容');
            return;
        }
        sendMessage(inputText);
    };
   
      return (
        <div className="container">
          <div className="content">
            {messages.map((msg, index) => (
              <div key={index} className="item item-right">
                <div className="bubble bubble-right">{msg.text}</div>
                <div className="avatar"><img src="https://pub.mayihr.com/AVATAR/u-c7916a43086943809b52b9f99e5a831f/OTFCNTRERUQtMTI2NC00RUUzLUI2MzgtNEVDRkFBOUI3QjREXzE2NjMxNjk3Njg0NDg5ODk=.jpeg"></img></div>
              </div>
            ))}
          </div>
          <div className="input-area">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              id="textarea"
            />
            <div className="button-area">
              <button id="send-btn" onClick={send}>
                发送
              </button>
            </div>
          </div>
        </div>
      );
    };

export default Chat;
