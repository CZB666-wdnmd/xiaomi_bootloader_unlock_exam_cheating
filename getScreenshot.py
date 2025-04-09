from PIL import ImageGrab
from io import BytesIO
import os
from PIL import Image

def getScreenshot():
    try:
        clipboard_content = ImageGrab.grabclipboard()
        if clipboard_content is None:
            clipboard_image = None
        elif isinstance(clipboard_content, list):
            # 如果剪贴板上有文件，检查第一个文件是否为png类型
            if len(clipboard_content) > 0 and os.path.splitext(clipboard_content[0])[1].lower() == ".png":
                try:
                    clipboard_image = Image.open(clipboard_content[0])
                except Exception:
                    clipboard_image = None
            else:
                clipboard_image = None
        else:
            clipboard_image = clipboard_content
        if clipboard_image is not None:
            buffer = BytesIO()
            clipboard_image.save(buffer, format="PNG")
            return buffer.getvalue()
        else:
            print("剪贴板中未找到图像数据。")
    except Exception as e:
        print(f"错误: {e}")