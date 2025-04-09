# 小米高考作弊

使用阿里云OCR识别文字，并使用下面两个模型对题目进行推理：

- **通义千问 QvQ-Max**  
    尽管在推理时依赖自身逻辑，可能未能充分参考现有题库，仍具备一定的回答创造性。

- **Deepseek-R1**  
    能够完美匹配题库和规则，作为主推理引擎为题目生成准确答案。


## 文件说明

- **question_db.txt**  
    放置题库数据。

- **rules.txt**  
    存放当天规则。程序启动后，会自动截屏识别，无需手动生成。

- **config.json**  
    用于存储阿里云和 Deepseek 的 API 配置。

## 配置示例

```json
{
        "ALIBABA_CLOUD_ACCESS_KEY_ID": "",
        "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "",
        "DEEPSEEK_API_KEY": "",
        "DASHSCOPE_API_KEY": ""
}
```
