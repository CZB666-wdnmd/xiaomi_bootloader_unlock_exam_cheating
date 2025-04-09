from getNowRules import main as get_now_rules_main
from aliyunocr import AliOcr
from getScreenshot import getScreenshot
import threading
import os
import ctypes
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from getAiAnswer import askTwoAi


def rules():
    print("请截图进入后的规则，以便做题时使用")
    get_now_rules_main()
    print("规则已保存到 rules.txt")

def check_files():
    if not os.path.exists("question_db.txt"):
        messagebox.showerror("错误", "找不到 question_db.txt，请将题库放在当前目录下")
        root.destroy()
        return False
    else:
        if os.path.exists("rules.txt"):
            messagebox.showinfo("提示", "rules.txt 存在，直接开始，如果需要更新规则请删除 rules.txt")
        else:
            rules()
        return True

if __name__ == "__main__":
    def start_answering():
        # Run askTwoAi in a separate thread to avoid blocking the GUI.
        Thread(target=askTwoAi).start()
    check_files()
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("小米解锁资格考试助手")
    root.geometry("500x300")

    # Title label
    lbl_title = tk.Label(root, text="欢迎使用小米解锁资格考试助手", font=("Arial", 16))
    lbl_title.pack(pady=20)

    # Create button frame
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Start answering button
    btn_start = tk.Button(frame, text="获取截图进行答题", font=("Arial", 12), width=20, command=start_answering)
    btn_start.grid(row=0, column=0, padx=10, pady=5)

    # Exit button
    btn_exit = tk.Button(root, text="退出", font=("Arial", 12), width=12, command=root.quit)
    btn_exit.pack(pady=20)

    root.mainloop()
