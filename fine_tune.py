
# gpt-3.5_fine_tune

#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import os
import openai
import tempfile
import datetime
import time
import string



import os

# 升級 openai 庫
os.system('pip install openai --upgrade')

# 使用 curl 下載 clinic_qa.json 文件
os.system('curl  https://github.com/hong91511/fine_tuning/blob/main/coffeeshopprepare.jsonl')

import openai

# 設置您的 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# 創建 fine-tune 文件
openai.File.create(
  file=open("mydata.jsonl", "rb"),
  purpose='fine-tune'
)

# 列出文件
openai.File.list()

# 創建 fine-tuning 作業
openai.FineTuningJob.create(training_file="file-BhA5o5gmQRCx15KsK4zq97WI", model="davinci-002")

# 列出 fine-tuning 作業
openai.FineTuningJob.list(limit=10)

# 檢索 fine-tuning 作業事件
openai.FineTuningJob.retrieve("ft:davinci-002:prsonal:test1:9CcruKZv")

# 列出 fine-tuning 作業事件
openai.FineTuningJob.list_events(id="ft:davinci-002:prsonal:test1:9CcruKZv", limit=10)

# 創建聊天完成
completion = openai.ChatCompletion.create(
  model="davinci-002",
  messages=[
    {"role": "system", "content": "您現在扮演一個咖啡廳線上點餐助手"},
    {"role": "user", "content": "我想知道義式濃縮咖啡的價格"}
  ]
)

print(completion.choices[0].message.content)

# 創建帶有 fine-tuned 模型的聊天完成
completion2 = openai.ChatCompletion.create(
  model="ft:davinci-002:personal:test1:9CcruKZv",
  messages=[
    {"role": "system", "content": "您現在扮演一個咖啡廳線上點餐助手"},
    {"role": "user", "content": "蜂蜜拿鐵需要付多少錢"}
  ]
)

print(completion2.choices[0].message.content)


def GPT_response(text):
    response = openai.ChatCompletion.create(
        model="ft:davinci-002:personal:test1:9CcruKZv",
        messages=[
            {"role": "system", "content": "您現在扮演一個咖啡廳線上點餐助手"},
            {"role": "user", "content": text}
        ]
    )

    answer = response.choices[0].message.content

    # 去除回复文本中的標點符號
    answer = answer.translate(str.maketrans('', '', string.punctuation))

    return answer
