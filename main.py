from getNowRules import main as get_now_rules_main
from qwenmax import askQwen
from deepseek import askDeepseek
from aliyunocr import AliOcr
from getScreenshot import getScreenshot
import threading
import os
import ctypes


def rules():
    print("请截图进入后的规则，以便做题时使用")
    get_now_rules_main()
    print("规则已保存到 rules.txt")

def getQuestionImage():
    print("请截图题目")
    image = getScreenshot()
    return image

def askTwoAi():
    question_image = getQuestionImage()
    question = AliOcr.main(question_image)

    thread1 = threading.Thread(target=askQwen, args=(question_image,))
    thread2 = threading.Thread(target=askDeepseek, args=(question,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    

if __name__ == "__main__":
    print("欢迎使用小米解锁资格考试助手")
    if os.path.exists("question_db.txt"):
        print("question_db.txt 存在")
    else:
        print("找不到 question_db.txt，请将题库放在当前目录下")
        exit()
    
    if os.path.exists("rules.txt"):
        print("rules.txt 存在，直接开始，如果需要更新规则请删除 rules.txt")
        print("按下回车键开始")
        input()
    else:
        print("考试开始后请截图规则")
        print("按下回车键开始")
        input()
        rules()
        print("已获取规则")
    
    while True:
        i = input("截图问题后，按下回车键开始答题，按下 q 键退出")
        if i == ('q'):
            break
        askTwoAi()
    
    print("感谢使用小米解锁资格考试助手")
