import { useQuery } from '@tanstack/react-query';
import "./CBA.css"
const CBA = () => {
    const fetchData = async () => {
        const response = await fetch('http://localhost:5000/chat'); // 将'/your-api-endpoint' 替换为你的API端点
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      };
        const { data, isLoading, error } = useQuery(
          {
           queryKey:['init'], 
           queryFn:fetchData,
          },
          );
          console.log(data);
        if (isLoading) {
          return <div>Loading...</div>;
        }
      
        if (error) {
          return <div>Error: {error.message}</div>;
        }
      return (
        <div className='left'>
          <p className='p'>回应：{JSON.stringify(data.response)}</p>
          <p className='p'>情绪：{JSON.stringify(data.mood.join(","))}</p>
          <p className='p'>好感度：{JSON.stringify(data.favorability)}</p>
          <p className='p'>阶段：{JSON.stringify(data.state)}</p>
          <p className='p'>时间：{JSON.stringify(data.clock)}</p>
        </div>
      );
    }
export default CBA;