from aliyunocr import AliOcr
from PIL import ImageGrab
from io import BytesIO
from getScreenshot import getScreenshot
import tkinter as tk
import sys

image_array = []
rules = ""

def main():
    global rules, image_array

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("获取当日规则")

    status_label = tk.Label(root, text="请截图当日规则")
    status_label.pack(pady=10)

    def capture():
        global image_array
        try:
            image = getScreenshot()
            image_array.append(image)
            status_label.config(text="图像已保存到列表。")
        except Exception as e:
            status_label.config(text=f"错误: {e}")

    def delete_last():
        global image_array
        if image_array:
            image_array.pop()
            status_label.config(text="已删除列表中的最后一项。")
        else:
            status_label.config(text="列表为空，无法删除。")
    def process_and_quit():
        global rules, image_array
        for image in image_array:
            content = AliOcr.main(image)
            rules += content + "\n"
        with open("rules.txt", "w", encoding="utf-8") as file:
            file.write(rules)
        root.destroy()
        return

    capture_button = tk.Button(root, text="获取截图", command=capture)
    capture_button.pack(pady=5)

    delete_button = tk.Button(root, text="删除上一个", command=delete_last)
    delete_button.pack(pady=5)

    quit_button = tk.Button(root, text="保存并继续", command=process_and_quit)
    quit_button.pack(pady=5)

    root.mainloop()