import numpy as np
import openai

# 相似度阈值
SIMILARITY_THRESHOLD = 0.6

def cosine_similarity(a, b):
    """计算余弦相似度"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_similarity(input_text, file_text):
    """计算输入文本与文件文本的相似度"""
    # 获取输入文本嵌入
    embedding1 = openai.Embedding.create(
        input=input_text,
        model="text-embedding-ada-002"
    )['data'][0]['embedding']

    # 获取文件文本嵌入
    embedding2 = openai.Embedding.create(
        input=file_text,
        model="text-embedding-ada-002"
    )['data'][0]['embedding']

    # 计算并返回余弦相似度
    return cosine_similarity(embedding1, embedding2)



