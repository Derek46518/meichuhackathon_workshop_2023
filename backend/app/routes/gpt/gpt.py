import openai

openai.api_key = "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"

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', 'AI']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text')

    except Exception as e:
        print('ERROR:', e)

    return text

def update_list(message: str, pl:list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str, pl: list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 2:]
    else:
        bot_response = 'Something went wrong'

    return bot_response

prompt_list: list[str] = ['You are a assistant of the company, which is very helpful, clever and kindly.']
def inputPrompt(userString):
    global prompt_list
    bot_printed = False  # 標誌，表示是否已經印出過"Bot:"
    
    user_input: str = userString
    response: str = get_bot_response(user_input, prompt_list)

        # 設定最大列寬度
    max_line_width = 60
    lines = [response[i:i + max_line_width] for i in range(0, len(response), max_line_width)]

    return lines[len(lines)-1]
    




