from aliyunocr import AliOcr
from openai import OpenAI
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import base64
import json
import threading
from getScreenshot import getScreenshot

def getQuestionImage():
    print("请截图题目")
    image = getScreenshot()
    return image

def askTwoAi() -> None:
    # 创建共享窗口并将左右两侧分别用于 Qwen 与 Deepseek 的回答显示
    window = tk.Tk()
    window.attributes("-topmost", True)
    window.title("两个 AI 的回答")

    # 使用网格布局创建两个 ScrolledText 小部件分别显示答案
    left_text = ScrolledText(window, width=50, height=80)
    left_text.grid(row=0, column=0, padx=10, pady=10)
    right_text = ScrolledText(window, width=50, height=80)
    right_text.grid(row=0, column=1, padx=10, pady=10)

    def run_qwen(question_image: bytes) -> None:
        with open("question_db.txt", "r", encoding="utf-8") as f:
            question_db = f.read()
        with open("rules.txt", "r", encoding="utf-8") as f:
            rules = f.read()
        with open("config.json", "r", encoding="utf-8") as f:
            config_data = json.load(f)
        api_key = config_data["DASHSCOPE_API_KEY"]
        client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

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
        准备好后进入分析模式，理解接下来发送的图片。
        """
        image_b64 = base64.b64encode(question_image).decode("utf-8")

        left_text.insert(tk.END, "\n" + "=" * 20 + " Qwen 思考过程 " + "=" * 20 + "\n")
        left_text.update()

        is_answering = False
        completion = client.chat.completions.create(
            model="qvq-max",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": question_db + "\n" + rules + "\n" +preset_prompt}]},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
                    {"type": "text", "text": preset_prompt+"解答这个问题"},
                ]}
            ],
            stream=True,
        )
        for chunk in completion:
            if not chunk.choices:
                left_text.insert(tk.END, "\nUsage:\n" + str(chunk.usage))
                left_text.update()
            else:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    left_text.insert(tk.END, delta.reasoning_content)
                    left_text.update()
                else:
                    if delta.content != "" and not is_answering:
                        left_text.insert(tk.END, "\n" + "=" * 20 + " Qwen 完整回复 " + "=" * 20 + "\n")
                        is_answering = True
                        left_text.update()
                    left_text.insert(tk.END, delta.content)
                    left_text.update()

    def run_deepseek(question: str):
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

        right_text.insert(tk.END, "\n" + "=" * 20 + " Deepseek 思考过程 " + "=" * 20 + "\n")
        right_text.update()

        is_answering = False
        completion = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[{"role": "user", "content": question_db+"\n"+rules+"\n"+preset_prompt+"\n"+question}],
            stream=True,
        )
        for chunk in completion:
            if not chunk.choices:
                right_text.insert(tk.END, "\nUsage:\n" + str(chunk.usage))
                right_text.update()
            else:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
                    right_text.insert(tk.END, delta.reasoning_content)
                    right_text.update()
                else:
                    if delta.content != "" and not is_answering:
                        right_text.insert(tk.END, "\n" + "=" * 20 + " Deepseek 完整回复 " + "=" * 20 + "\n")
                        is_answering = True
                        right_text.update()
                    right_text.insert(tk.END, delta.content)
                    right_text.update()

    question_image = getQuestionImage()
    if not question_image:
        print("No valid screenshot captured, exiting.")
        return
    
    question = AliOcr.main(question_image)
    t1 = threading.Thread(target=run_qwen, args=(question_image,))
    t2 = threading.Thread(target=run_deepseek, args=(question,))

    t1.start()
    t2.start()

    window.mainloop()