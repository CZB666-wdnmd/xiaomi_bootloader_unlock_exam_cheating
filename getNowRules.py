from aliyunocr import AliOcr
from PIL import ImageGrab
from io import BytesIO
from getScreenshot import getScreenshot

image_array = []
rules = ""

def main() -> str:
    global rules
    while True:
        i = input("按回车键以捕获剪贴板图像，按'q'退出,按'r'删除上一个: ")
        if i == ('q'):
            break
        elif i == ('r'):
            if image_array:
                image_array.pop()
                print("已删除列表中的最后一项。")
            else:
                print("列表为空，无法删除。")
        try:
            image_array.append(getScreenshot())
            print("图像已保存到列表。")
        except Exception as e:
            print(f"错误: {e}")
    for image in image_array:
            content = AliOcr.main(image)
            rules += content + "\n"
    with open("rules.txt", "w", encoding="utf-8") as file:
        file.write(rules)