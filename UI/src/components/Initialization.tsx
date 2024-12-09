import ABC from "../components/ABC";
import Chat from "../components/Chat";
import CBA from "../components/CBA";
const Initialization: React.FC = () => {
 
    const fetch1 = async () => {
      try {
        await fetch("http://127.0.0.1:8000/init", { method: "POST" });
      } catch (error) {
        console.log(error);
      }
    };
    const fetchData=() => {
     fetch1();
    };
  return (
    <>
    <div>
      <button className="a" onClick={fetchData}>初始化游戏</button>
      <button className="a" onClick={() => window.location.reload()}>更新</button>
      <ABC />
      <CBA />
      <Chat />
    </div>
    </>
  );
};

export default Initialization;
