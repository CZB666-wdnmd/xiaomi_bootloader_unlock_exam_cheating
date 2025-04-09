import os
import sys
import json

from typing import List

from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

class AliOcr:
    def __init__(self):
        pass

    def create_client() -> ocr_api20210707Client:
        with open("config.json", "r", encoding="utf-8") as f:
            config_data = json.load(f)
        config = open_api_models.Config(
            access_key_id=config_data["ALIBABA_CLOUD_ACCESS_KEY_ID"],
            access_key_secret=config_data["ALIBABA_CLOUD_ACCESS_KEY_SECRET"]
        )
        config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
        return ocr_api20210707Client(config)

    @staticmethod
    def main(
        img_binary: bytes,
    ) -> None:
        client = AliOcr.create_client()
        recognize_advanced_request = ocr_api_20210707_models.RecognizeAdvancedRequest(
            need_sort_page=True,
            paragraph=True,
            body=img_binary
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.recognize_advanced_with_options(recognize_advanced_request, runtime)
            qust = json.loads(resp.body.to_map()["Data"])["prism_paragraphsInfo"]
            result = "\n".join(f"{item['word']}" for item in qust)
            return result

        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
