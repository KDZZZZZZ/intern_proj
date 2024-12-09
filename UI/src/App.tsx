import { useState } from "react";
import "./App.css";
import Initialization from "./components/Initialization";
import Front from "./components/Chat";
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
           Welcome to OpenStarRail
          </div>

          {/* 初始化页面 */}
          {currentSection === "initialization" && (
            <section className="section">
              <Initialization />
            </section>
          )}

        </>
      )}
    </div>
  );
}

export default App;





