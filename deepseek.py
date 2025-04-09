from aliyunocr import AliOcr
from openai import OpenAI
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import json


def askDeepseek(question: str) -> None:
    with open("question_db.txt", "r", encoding="utf-8") as f:
        question_db = f.read()
    with open("rules.txt", "r", encoding="utf-8") as f:
        rules = f.read()
    with open("config.json", "r", encoding="utf-8") as f:
        config_data = json.load(f)
    api_key = config_data["DEEPSEEK_API_KEY"]
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    preset_prompt = """
    你现在是一个专业考试助理，我给你提供了“小米 BootLoader 解锁资格考试”的题库与当天考试规则。你需要严格按照我提供的题库和规则来进行答题分析和解答。
    请务必注意以下几点：
    以我提供的题库为唯一标准，如果你的知识与你的认知有冲突，请以题库为准；
    认真审题，注意题目是单选还是多选，不要选错数量；
    尤其要警惕陷阱题，例如多重否定、特殊限制条件等；
    你的任务是根据题目选项，结合题库分析选出最合理的答案，并简要说明理由；
    不要凭空补充题库外的知识内容，严格在题库范围内答题；
    如果题目中有数学计算或逻辑推理，请善用你的推理能力解决它；
    你需要以最快的思考速度解决这个问题，如果有摸棱两可的选项，请直接选择最优解，不要犹豫，这个考试是限时的；
    准备好后进入分析模式。
    """

    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复

    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": question_db+"\n"+rules+"\n"+preset_prompt+"\n"+question}],
        stream=True,
    )

    # 创建新窗口显示输出内容
    output_window = tk.Tk()
    output_window.wm_attributes("-topmost", 1)
    output_window.title("Deepseek")
    text_area = ScrolledText(output_window, width=100, height=30)
    text_area.pack(fill=tk.BOTH, expand=True)

    text_area.insert(tk.END, "\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    output_window.update()

    for chunk in completion:
        # 如果chunk.choices为空，则将usage写入窗口
        if not chunk.choices:
            text_area.insert(tk.END, "\nUsage:\n")
            text_area.insert(tk.END, str(chunk.usage))
            output_window.update()
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                text_area.insert(tk.END, delta.reasoning_content)
                reasoning_content += delta.reasoning_content
                output_window.update()
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    text_area.insert(tk.END, "\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                    output_window.update()
                # 打印回复过程
                text_area.insert(tk.END, delta.content)
                answer_content += delta.content
                output_window.update()

    output_window.mainloop()

