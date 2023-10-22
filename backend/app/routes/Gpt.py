import pandas as pd
import tiktoken
import openai
import numpy as np
import math
import os
import argparse
openai.api_key="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"

encoding = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('./csvData/update_late_employees_sorted.csv')
df = df.dropna()
df = df[["EmpId", "EmpShift", "DeptId", "Zone", "DateTime"]]
df["summarized"] = (
            df.EmpId.str.strip() + " " + df.EmpShift.str.strip() + " " + df.DeptId.str.strip() + " " + df.Zone.str.strip() + " " + df.DateTime.str.strip() + ";")
df["tokens"] = df.summarized.apply(lambda x: len(encoding.encode(x)))

def get_api_response(prompt: str) -> str | None:
    text: str | None = None
    array = []
    array.append({"role": "user", "content": prompt})

    try:

        response: dict = openai.ChatCompletion.create(
            model='gpt-4',
            messages=array,
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=['user:', 'assistant']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('message').get('content')

    except Exception as e:
        print('ERROR:', e)

    return text


def update_list(message: str, pl: list[dict]):
    pl.append(message)


def create_prompt(message: str, pl: list[dict]) -> str:
    p_messages = [item.get("content") for item in pl]  # Extract "content" from dictionaries
    p_messages.append(f'\nuser: {message}')
    prompt = ''.join(p_messages)
    return prompt


'''
def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nuser: {message}'
    update_list(p_message, pl)
    print(type(pl))
    prompt: str = ''.join(pl)
    return prompt
'''


def get_bot_response(message: str, pl: list[dict]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nassistant: ')
    else:
        bot_response = 'Something went wrong'

    return bot_response


def main():
    prompt_list = []
    prompt_list.append({
        "role": "user",
        "content": "根據以下輸入整理出誰是9/19遲到的員工\nEmpID是員工ID\nShiftTime是員工應到時間\nDeptID是員工所述部門ID\nZone是員工所屬廠區\nDateTime是員工當天上班時間\n一個員工當然可能在不同天遲到\nEmpId,EmpShift,DeptId,Zone,DateTime\nEMP054,08:30,DEPT4,HQ,/9/12  09:02:00 \nEMP112,08:30,DEPT2,HQ,/9/12  09:01:00 \nEMP094,08:30,DEPT3,HQ,/9/12  09:04:00 \nEMP023,07:30,DEPT4,HQ,/9/13  08:01:00 \nEMP022,07:30,DEPT4,HQ,/9/13  08:14:00 \nEMP051,08:30,DEPT3,HQ,/9/13  09:03:00 \nEMP160,09:30,DEPT3,HQ,/9/13  10:06:00 \nEMP187,09:30,DEPT4,HQ,/9/13  10:03:00 \nEMP040,08:30,DEPT4,HQ,/9/14  09:04:00 \nEMP045,08:30,DEPT4,HQ,/9/14  09:03:00 \nEMP189,09:30,DEPT4,HQ,/9/14  10:04:00 \nEMP015,07:30,DEPT4,HQ,/9/15  08:04:00 \nEMP006,07:30,DEPT4,HQ,/9/15  08:01:00 \nEMP096,08:30,DEPT4,HQ,/9/15  09:01:00 \nEMP060,08:30,DEPT4,HQ,/9/15  09:01:00 \nEMP131,08:30,DEPT3,HQ,/9/15  09:03:00 \nEMP179,09:30,DEPT4,HQ,/9/15  10:02:00 \nEMP167,09:30,DEPT2,HQ,/9/15  10:01:00 \nEMP138,09:30,DEPT1,HQ,/9/18  10:01:00 \nEMP187,09:30,DEPT4,HQ,/9/18  10:11:00 \nEMP072,08:30,DEPT2,HQ,/9/19  09:04:00 \nEMP080,08:30,DEPT4,HQ,/9/19  09:06:00 \nEMP048,08:30,DEPT4,HQ,/9/19  09:05:00 \nEMP113,08:30,DEPT4,HQ,/9/19  09:10:00 \nEMP158,09:30,DEPT4,HQ,/9/19  10:01:00 \nEMP174,09:30,DEPT4,HQ,/9/20  10:05:00 \nEMP018,07:30,DEPT4,HQ,/9/21  08:03:00 \nEMP091,08:30,DEPT4,HQ,/9/21  09:06:00 \nEMP121,08:30,DEPT4,HQ,/9/21  09:06:00 \nEMP041,08:30,DEPT4,HQ,/9/21  09:05:00 \nEMP168,09:30,DEPT3,HQ,/9/21  10:04:00 \nEMP017,07:30,DEPT4,HQ,/9/22  08:05:00 \nEMP094,08:30,DEPT3,HQ,/9/22  09:03:00 \nEMP066,08:30,DEPT1,HQ,/9/22  09:04:00 \nEMP162,09:30,DEPT2,HQ,/9/22  10:01:00 \nEMP187,09:30,DEPT4,HQ,/9/22  10:07:00 \nEMP259,08:30,DEPT2,AZ,/9/11  09:08:00 \nEMP257,08:30,DEPT3,AZ,/9/12  09:09:00 \nEMP297,08:30,DEPT1,AZ,/9/12  09:12:00 \nEMP205,06:30,DEPT3,AZ,/9/13  07:10:00 \nEMP226,08:30,DEPT3,AZ,/9/13  09:02:00 \nEMP231,08:30,DEPT3,AZ,/9/13  09:05:00 \nEMP258,08:30,DEPT4,AZ,/9/13  09:03:00 \nEMP261,08:30,DEPT4,AZ,/9/13  09:18:00 \nEMP263,08:30,DEPT3,AZ,/9/13  09:09:00\nEMP265,08:30,DEPT3,AZ,/9/13  09:03:00 \nEMP285,08:30,DEPT3,AZ,/9/13  09:11:00 \nEMP287,08:30,DEPT1,AZ,/9/13  09:01:00 \nEMP309,08:30,DEPT4,AZ,/9/13  09:01:00 \nEMP321,08:30,DEPT4,AZ,/9/13  09:04:00 \nEMP336,08:30,DEPT3,AZ,/9/13  09:01:00 \nEMP366,09:00,DEPT1,AZ,/9/13  09:53:00 \nEMP374,09:00,DEPT4,AZ,/9/13  09:31:00 \nEMP399,09:00,DEPT1,AZ,/9/13  09:33:00 \nEMP206,06:30,DEPT4,AZ,/9/14  07:04:00 \nEMP210,06:30,DEPT3,AZ,/9/14  07:01:00 \nEMP228,08:30,DEPT3,AZ,/9/14  09:04:00 \nEMP230,08:30,DEPT1,AZ,/9/14  09:15:00 \nEMP233,08:30,DEPT2,AZ,/9/14  09:01:00 \nEMP234,08:30,DEPT1,AZ,/9/14  09:05:00 \nEMP239,08:30,DEPT2,AZ,/9/14  09:01:00 \nEMP240,08:30,DEPT3,AZ,/9/14  09:08:00 \nEMP241,08:30,DEPT4,AZ,/9/14  09:04:00 \nEMP256,08:30,DEPT2,AZ,/9/14  09:13:00 \nEMP261,08:30,DEPT4,AZ,/9/14  09:02:00 \nEMP273,08:30,DEPT2,AZ,/9/14  09:05:00 \nEMP324,08:30,DEPT4,AZ,/9/14  09:04:00 \nEMP342,08:30,DEPT4,AZ,/9/14  09:02:00 \nEMP372,09:00,DEPT1,AZ,/9/14  09:33:00 \nEMP218,06:30,DEPT3,AZ,/9/15  07:06:00 \nEMP251,08:30,DEPT1,AZ,/9/15  09:15:00 \nEMP254,08:30,DEPT3,AZ,/9/15  09:05:00 \nEMP269,08:30,DEPT4,AZ,/9/15  09:06:00 \nEMP273,08:30,DEPT2,AZ,/9/15  09:03:00 \nEMP293,08:30,DEPT4,AZ,/9/15  09:05:00 \nEMP297,08:30,DEPT1,AZ,/9/15  09:01:00 \nEMP308,08:30,DEPT2,AZ,/9/15  09:08:00 \nEMP321,08:30,DEPT4,AZ,/9/15  09:10:00 \nEMP344,08:30,DEPT4,AZ,/9/15  09:08:00 \nEMP348,08:30,DEPT4,AZ,/9/15  09:07:00 \nEMP356,09:00,DEPT4,AZ,/9/15  09:41:00 \nEMP368,09:00,DEPT3,AZ,/9/15  09:31:00 \nEMP234,08:30,DEPT1,AZ,/9/18  09:16:00 \nEMP266,08:30,DEPT2,AZ,/9/18  09:07:00 \nEMP267,08:30,DEPT3,AZ,/9/18  09:07:00 \nEMP270,08:30,DEPT4,AZ,/9/18  09:13:00 \nEMP293,08:30,DEPT4,AZ,/9/18  09:08:00 \nEMP304,08:30,DEPT4,AZ,/9/18  09:09:00 \nEMP333,08:30,DEPT2,AZ,/9/18  09:02:00 \nEMP337,08:30,DEPT4,AZ,/9/18  09:01:00 \nEMP342,08:30,DEPT4,AZ,/9/18  09:01:00 \nEMP374,09:00,DEPT4,AZ,/9/18  09:37:00 \nEMP391,09:00,DEPT4,AZ,/9/18  09:34:00 \nEMP397,09:00,DEPT1,AZ,/9/18  09:48:00 \nEMP203,06:30,DEPT1,AZ,/9/19  07:09:00 \nEMP229,08:30,DEPT4,AZ,/9/19  09:15:00 \nEMP231,08:30,DEPT3,AZ,/9/19  09:12:00 \nEMP234,08:30,DEPT1,AZ,/9/19  09:05:00 \nEMP239,08:30,DEPT2,AZ,/9/19  09:04:00 \nEMP244,08:30,DEPT4,AZ,/9/19  09:03:00 \nEMP248,08:30,DEPT4,AZ,/9/19  09:14:00 \nEMP264,08:30,DEPT4,AZ,/9/19  09:07:00 \nEMP273,08:30,DEPT2,AZ,/9/19  09:12:00 \nEMP298,08:30,DEPT4,AZ,/9/19  09:04:00 \nEMP314,08:30,DEPT4,AZ,/9/19  09:10:00 \nEMP316,08:30,DEPT4,AZ,/9/19  09:09:00 \nEMP356,09:00,DEPT4,AZ,/9/19  09:36:00 \nEMP400,09:00,DEPT2,AZ,/9/19  09:40:00 \nEMP230,08:30,DEPT1,AZ,/9/20  09:20:00 \nEMP245,08:30,DEPT1,AZ,/9/20  09:22:00 \nEMP255,08:30,DEPT3,AZ,/9/20  09:20:00 \nEMP289,08:30,DEPT2,AZ,/9/20  09:01:00 \nEMP299,08:30,DEPT3,AZ,/9/20  09:02:00 \nEMP321,08:30,DEPT4,AZ,/9/20  09:03:00 \nEMP330,08:30,DEPT4,AZ,/9/20  09:12:00 \nEMP362,09:00,DEPT4,AZ,/9/20  09:33:00 \nEMP373,09:00,DEPT3,AZ,/9/20  09:37:00 \nEMP375,09:00,DEPT3,AZ,/9/20  09:40:00 \nEMP398,09:00,DEPT4,AZ,/9/20  09:44:00 \nEMP203,06:30,DEPT1,AZ,/9/21  07:10:00 \nEMP211,06:30,DEPT4,AZ,/9/21  07:01:00 \nEMP217,06:30,DEPT3,AZ,/9/21  07:11:00 \nEMP230,08:30,DEPT1,AZ,/9/21  09:02:00 \nEMP234,08:30,DEPT1,AZ,/9/21  09:03:00 \nEMP247,08:30,DEPT1,AZ,/9/21  09:15:00 \nEMP250,08:30,DEPT2,AZ,/9/21  09:22:00 \nEMP275,08:30,DEPT4,AZ,/9/21  09:11:00 \nEMP287,08:30,DEPT1,AZ,/9/21  09:05:00 \nEMP289,08:30,DEPT2,AZ,/9/21  09:01:00 \nEMP302,08:30,DEPT4,AZ,/9/21  09:01:00 \nEMP305,08:30,DEPT1,AZ,/9/21  09:02:00 \nEMP314,08:30,DEPT4,AZ,/9/21  09:17:00 \nEMP390,09:00,DEPT4,AZ,/9/21  09:32:00 \nEMP398,09:00,DEPT4,AZ,/9/21  09:56:00 \nEMP399,09:00,DEPT1,AZ,/9/21  09:32:00 \nEMP219,06:30,DEPT2,AZ,/9/22  07:01:00 \nEMP241,08:30,DEPT4,AZ,/9/22  09:18:00 \nEMP243,08:30,DEPT3,AZ,/9/22  09:08:00 \nEMP248,08:30,DEPT4,AZ,/9/22  09:04:00 \nEMP259,08:30,DEPT2,AZ,/9/22  09:07:00 \nEMP262,08:30,DEPT4,AZ,/9/22  09:06:00 \nEMP277,08:30,DEPT2,AZ,/9/22  09:01:00 \nEMP284,08:30,DEPT4,AZ,/9/22  09:17:00 \nEMP289,08:30,DEPT2,AZ,/9/22  09:04:00 \nEMP322,08:30,DEPT4,AZ,/9/22  09:13:00 \nEMP329,08:30,DEPT3,AZ,/9/22  09:14:00 \nEMP333,08:30,DEPT2,AZ,/9/22  09:12:00 \n"
    })
    prompt_list.append({
        "role": "assistant",
        "content": "在9/19這天遲到的員工有：\n\nHQ廠區：\nEMP072, EMP080, EMP048, EMP113\n\nAZ廠區：\nEMP229, EMP231, EMP234, EMP239, EMP244, EMP248, EMP264, EMP273, EMP298, EMP314, EMP316, EMP356, EMP400"
    })

    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, prompt_list)
        # print(f'Bot: {response}')
        print(f'{response}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    opt = parser.parse_args()