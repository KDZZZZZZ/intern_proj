import openai
import stimulate
openai.api_key = '你的API密钥'
import random
import history
import numpy as np

# 阈值设定
similarity_THRESHOLD = 0.6
# 设计一个取出机制，根据概率随机取出一个文本
def get_random_text():
    texts = list(history.file_probabilities.keys())
    probabilities = list(history.file_probabilities.values())
    return random.choices(texts, probabilities)[0]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
# 获取文本嵌入

def get_similarity():
    embeddings1 = openai.Embedding.create(
        input="第一段文本",#在这里插入对话的内容
        model="text-embedding-ada-002"
    )['data'][0]['embedding']

    embeddings2 = openai.Embedding.create(
        input=get_random_text(),
        model="text-embedding-ada-002"
    )['data'][0]['embedding']
    return cosine_similarity(embeddings1, embeddings2)

if stimulate.should_activate:
    if get_similarity() > similarity_THRESHOLD:{}
        #在生成对话的提示词的模块调用similar_text


