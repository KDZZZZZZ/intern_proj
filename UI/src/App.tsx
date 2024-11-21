import React, { useState } from "react";
import "./App.css";
import Initialization from "./components/Initialization";
import DailyInteraction from "./components/DailyInteraction";

function App() {
  const [isWelcomePage, setIsWelcomePage] = useState(true); // 状态控制是否显示欢迎页
  const [currentSection, setCurrentSection] = useState<"initialization" | "daily">("initialization");

  // 点击事件处理函数
  const handleWelcomeClick = () => {
    setIsWelcomePage(false); // 隐藏欢迎页，进入主功能页面
  };

  return (
    <div className="App">
      {/* 欢迎页面 */}
      {isWelcomePage ? (
        <div className="welcome-page" onClick={handleWelcomeClick}>
          <h1>welcome to try something we create</h1>
          <p>please click</p>
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
          </div>

          {/* 初始化界面 */}
          {currentSection === "initialization" && (
            <section className="section">
              <h2>Initialization Section</h2>
              <Initialization />
            </section>
          )}

          {/* 日常交互界面 */}
          {currentSection === "daily" && (
            <section className="section">
              <h2>Daily Interaction Section</h2>
              <DailyInteraction />
            </section>
          )}
        </>
      )}
    </div>
  );
}

export default App;



