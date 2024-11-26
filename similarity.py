import requests
from typing import List, Dict, Union, Optional
import time
import os
import glob
import chardet

class TextSimilarity:
    """文本相似度计算类"""
    
    def __init__(self, api_key: str, 
                 model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 max_retries: int = 3,
                 retry_delay: float = 1.0,
                 history_dir: str = "history"):
        """
        初始化TextSimilarity类
        
        Args:
            api_key: HuggingFace API密钥
            model: 要使用的模型名称
            max_retries: 最大重试次数
            retry_delay: 重试间隔（秒）
            history_dir: 历史记录存储目录
        """
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.history_dir = history_dir

    def calculate_similarity(self, 
                           source_text: str, 
                           target_texts: Union[str, List[str]],
                           threshold: Optional[float] = None) -> Dict:
        """
        计算源文本与目标文本之间的相似度
        
        Args:
            source_text: 源文本
            target_texts: 目标文本或目标文本列表
            threshold: 相似度阈值，只返回相似度大于此值的结果
            
        Returns:
            Dict: 包含相似度分数的字典
            {
                "scores": [float],  # 相似度分数列表
                "filtered_results": [  # 如果设置了threshold，则包含此字段
                    {"text": str, "score": float}  # 过滤后的结果
                ]
            }
        """
        if isinstance(target_texts, str):
            target_texts = [target_texts]
            
        payload = {
            "inputs": {
                "source_sentence": source_text,
                "sentences": target_texts
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.api_url, 
                                      headers=self.headers, 
                                      json=payload,
                                      timeout=30)
                response.raise_for_status()
                scores = response.json()
                
                result = {"scores": scores}
                
                # 如果设置了阈值，添加过滤后的结果
                if threshold is not None:
                    filtered_results = [
                        {"text": text, "score": score}
                        for text, score in zip(target_texts, scores)
                        if score >= threshold
                    ]
                    result["filtered_results"] = filtered_results
                
                return result
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"API请求失败: {str(e)}")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                raise Exception(f"计算相似度时发生错误: {str(e)}")

    def find_most_similar(self, 
                         source_text: str, 
                         target_texts: List[str],
                         top_k: int = 1) -> List[Dict]:
        """
        找出与源文本最相似的几个目标文本
        
        Args:
            source_text: 源文本
            target_texts: 目标文本列表
            top_k: 返回相似度最高的前k个结果
            
        Returns:
            List[Dict]: 包含最相似文本及其分数的列表
            [
                {"text": str, "score": float}
            ]
        """
        result = self.calculate_similarity(source_text, target_texts)
        scores = result["scores"]
        
        # 将文本和分数配对，并按分数排序
        text_scores = list(zip(target_texts, scores))
        text_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前k个结果
        return [
            {"text": text, "score": score}
            for text, score in text_scores[:top_k]
        ]

    def get_history_texts(self, stage: Optional[int] = None) -> List[str]:
        """
        从历史记录文件中获取文本
        
        Args:
            stage: 如果指定，则读取从stage到stage_1的所有文本
                  如果不指定，则读取所有stage文件
        
        Returns:
            List[str]: 历史记录中的文本列表
        """
        if not os.path.exists(self.history_dir):
            return []

        if stage is not None:
            # 从stage到1的所有文件
            files = []
            for i in range(stage, 0, -1):
                file_path = os.path.join(self.history_dir, f"stage_{i}.txt")
                if os.path.exists(file_path):
                    files.append(file_path)
        else:
            # 所有stage文件
            file_pattern = os.path.join(self.history_dir, "stage_*.txt")
            files = sorted(glob.glob(file_pattern), 
                         key=lambda x: int(x.split('_')[-1].split('.')[0]),
                         reverse=True)

        texts = []
        for file_path in files:
            try:
                # 先读取文件内容并检测编码
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] if result['encoding'] else 'utf-8'
                
                # 解码内容
                content = raw_data.decode(encoding).strip()
                
                # 重新以UTF-8编码写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                if content:
                    texts.extend(content.split('\n'))
                    print(f"已读取并修正文件编码: {file_path}")
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {str(e)}")

        return [text.strip() for text in texts if text.strip()]

    def find_similar_in_history(self,
                              source_text: str,
                              stage: Optional[int] = None,
                              top_k: int = 1,
                              threshold: Optional[float] = None) -> List[Dict]:
        """在历史记录中查找与输入文本最相似的内容"""
        history_texts = self.get_history_texts(stage)
        if not history_texts:
            return []

        result = self.calculate_similarity(source_text, history_texts, threshold)
        
        if threshold is not None and "filtered_results" in result:
            filtered = result["filtered_results"]
            filtered.sort(key=lambda x: x["score"], reverse=True)
            return filtered[:top_k]
        else:
            return self.find_most_similar(source_text, history_texts, top_k)

# 使用示例
if __name__ == "__main__":
    similarity = TextSimilarity(api_key="hf_xxxx")
    
    # 基本使用
    source = "That is a happy person"
    targets = [
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day"
    ]
    
    # 计算相似度
    result = similarity.calculate_similarity(source, targets)
    print("所有相似度分数:", result["scores"])
    
    # 使用阈值过滤
    result = similarity.calculate_similarity(source, targets, threshold=0.8)
    print("高相似度结果:", result["filtered_results"])
    
    # 找出最相似的2个文本
    most_similar = similarity.find_most_similar(source, targets, top_k=2)
    print("最相似的文本:", most_similar)

    # 从历史记录中查找相似内容
    similar_texts = similarity.find_similar_in_history(
        source_text="你好，今天天气真好",
        stage=1,  # 可选：指定阶段
        top_k=2,  # 返回最相似的2条记录
        threshold=0.8  # 只返回相似度>=0.8的结果
    )
    print("历史记录中的相似内容:", similar_texts)
