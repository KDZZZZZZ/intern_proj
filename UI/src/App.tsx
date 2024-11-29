import { useState } from "react";
import "./App.css";
import Initialization from "./components/Initialization";
import DailyInteraction from "./components/DailyInteraction";
import ChatPage from "./components/ChatPage";

function App() {
  const [isWelcomePage, setIsWelcomePage] = useState(true); // 控制欢迎页状态
  const [currentSection, setCurrentSection] = useState<"initialization" | "daily" | "chat">("initialization");

  const handleWelcomeClick = () => {
    setIsWelcomePage(false); // 隐藏欢迎页面
  };

  return (
    <div className="App">
      {/* 欢迎页面 */}
      {isWelcomePage ? (
        <div className="welcome-page" onClick={handleWelcomeClick}>
          <h1>欢迎来到我的应用！</h1>
          <p>点击任意位置开始体验</p>
        </div>
      ) : (
        <>
          {/* 导航部分 */}
          <div className="navigation">
            <button
              onClick={() => setCurrentSection("initialization")}
              className={currentSection === "initialization" ? "active" : ""}
            >
              Initialization
            </button>
            <button
              onClick={() => setCurrentSection("daily")}
              className={currentSection === "daily" ? "active" : ""}
            >
              Daily Interaction
            </button>
            <button
              onClick={() => setCurrentSection("chat")}
              className={currentSection === "chat" ? "active" : ""}
            >
              Chat Page
            </button>
          </div>

          {/* 初始化页面 */}
          {currentSection === "initialization" && (
            <section className="section">
              <Initialization />
            </section>
          )}

          {/* 日常交互页面 */}
          {currentSection === "daily" && (
            <section className="section">
              <DailyInteraction />
            </section>
          )}

          {/* 对话页面 */}
          {currentSection === "chat" && (
            <section className="section">
              <ChatPage />
            </section>
          )}
        </>
      )}
    </div>
  );
}

export default App;





