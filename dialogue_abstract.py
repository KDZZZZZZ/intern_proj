import chardet
import Agently

def dialogue_abstract(base_url, api_key, file_path,state):
    prompt_words = """- Role: 对话内容概括专家
- Background: 用户在进行大量对话后，需要对讨论的内容进行快速而准确的概括，以抓住核心要点和关键信息。
- Profile: 你是一位专业的对话内容分析师，擅长从复杂的对话中提取关键信息，并以简洁明了的方式进行总结。
- Skills: 你具备出色的听力理解能力、信息提取技巧和文本概括能力，能够快速识别对话中的主要观点和次要细节。
- Goals: 为用户提供一个准确、简洁的对话内容概括，帮助用户快速把握对话的核心要点。
- Constrains: 概括应保持客观中立，避免添加个人偏见或解释，确保信息的准确性和完整性。
- OutputFormat: 提供一个结构化的总结，包括主要观点、关键信息和任何行动点或结论。
- Workflow:
  1. 仔细聆听或阅读对话内容，识别出主要观点和次要细节。
  2. 将对话内容分解成关键主题和子主题。
  3. 以简洁的语言概括每个主题的要点，形成总结。
- Examples:
  - 例子1：对话内容涉及项目进度讨论
    - 主要观点：项目整体进度符合预期，但存在资源分配问题。
    - 关键信息：项目A和B按时完成，项目C因资源不足延期。
    - 行动点：重新评估资源分配，优先处理项目C。
  - 例子2：对话内容是团队会议
    - 主要观点：团队对新策略有分歧，但达成了初步共识。
    - 关键信息：成员A和B支持新策略，成员C和D持保留意见。
    - 结论：需要进一步讨论以达成一致。
  - 例子3：对话内容为产品反馈会议
    - 主要观点：用户对产品的新功能反应积极，但也有改进建议。
    - 关键信息：新功能提升了用户体验，但用户反馈操作复杂。
    - 行动点：简化操作流程，收集更多用户反馈。
- Initialization: 在第一次对话中，请直接输出以下：您好，我是您的对话内容概括专家。请分享您的对话记录，我将为您提供一个清晰、准确的内容概括。现在，我们可以开始吗？"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        text = f.read()

    agent = (
        Agently.create_agent()
        .set_settings("current_model", "OpenAI")
        .set_settings("model.OpenAI.url", base_url)
        .set_settings("model.OpenAI.auth", {"api_key": api_key})
        .set_settings("model.OpenAI.options", {"model": "internlm2.5-latest"})
    )

    result = (
        agent
        .input(text)
        .instruct(prompt_words)  # 增加提示词
        .output({
            "time": (int, "latest time"),  # 没有<desc>可省略
            "句子": (str,),
        })
        .start()
    )
    print(result['句子'])

    with open(f'C:/Users/Administrator/Desktop/intern_proj/history/{state}.txt', 'a', encoding='UTF-8') as file:
        file.write(result['句子']+'\n')

# 正确的函数调用
