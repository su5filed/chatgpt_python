# chat gpt と　Bard
import openai
from tkinter import messagebox, simpledialog, Tk
import PySimpleGUI as sg

from bardapi import Bard

api_key = 'sk-.....'
openai.api_key = api_key

#chat GPTの応答
def generate_text_chatgpt(prompt, conversation_history):
    # プロンプトを会話履歴に追加
    conversation_history.append({"role": "user", "content": prompt})

    # GPT-4モデルを使用する場合
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        # model="gpt-4-model",
        # model="gpt-3.5-turbo",
        messages=conversation_history
    )
    message = ""

    for choice in response.choices:
        message += choice.message['content']

    # 応答文を会話履歴に追加
    conversation_history.append({"role": "assistant", "content": message})
    return message

# bardの応答
def generate_text_bard(prompt, conversation_history_bard):    
    token = 'xxxxxx-xxxxx.' #os.environ['COOKIE_TOKEN']
    bard = Bard(token=token)
    # prompt="LLMとはなんですか?"
    print("generate_text_bard...")
    response = bard.get_answer(prompt)['content']
    print(response)
    conversation_history_bard.append(response)
    return response


def show_dialog():
    # ウィンドウのテーマ
    sg.theme('BlueMono')


    # ウィンドウの初期サイズ
    initial_width = 600
    initial_height = 20
    #width = 600
    #height = 20

    # ウィンドウのレイアウト
    layout = [
            [sg.Button('SEND', size=(10, 1), key='SEND'),sg.Button('CLEAR', size=(10, 1), key='CLEAR'),sg.Button('CLOSE', size=(10, 1), key='CLOSE') ],
            [sg.Multiline(default_text="", size=(initial_width,5),  key='Multiline1') ],
            [sg.Multiline(default_text="", size=(initial_width,10), key='Multiline2') ],
            [sg.Multiline(default_text="", size=(initial_width,10), key='Multiline3') ],
        ]

    # ウィンドウオブジェクトの作成
    window = sg.Window('title', layout, size=(700, 480), resizable=True)

    # 会話履歴を格納するためのリストを初期化
    conversation_history = []
    conversation_history_bard = []

    # イベントのループ
    while True:
        # イベントの読み込み
        event, values = window.read()
        # 変更部分
        print('Event: ', event)
        print('values: ', values)
        
        # 変更部分終わり
        if event == 'CLOSE':
            break

        if event == 'CLEAR':
            window['Multiline1'].update("")

        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break
        
        if( event == 'SEND' and len(values) > 0 ):
            input_prompt = values['Multiline1']
            generated_text = generate_text_chatgpt(input_prompt, conversation_history)
            window['Multiline2'].update(generated_text)
            print("応答 chatgpt:", generated_text)
            generated_text = generate_text_bard(input_prompt, conversation_history_bard)
            window['Multiline3'].update(generated_text)
            print("応答 bard:", generated_text)
        
        
        # ウィンドウのサイズ変更イベントの場合
        if event == '__TIMEOUT__':
            # ウィンドウのサイズを取得
            window_width, window_height = window.size
            print("window_height:", window_height)
            
            # Multiline1とMultiline2の高さを比率に応じて調整
            new_height1 = (window_height - initial_height) // 3  # Multiline1の新しい高さ
            new_height2 = (window_height - initial_height) // 3 * 2  # Multiline2の新しい高さ

            # Multiline1とMultiline2の高さを変更
            window['Multiline1'].Update(size=(window_width, new_height1))
            window['Multiline2'].Update(size=(window_width, new_height2))
            window['Multiline3'].Update(size=(window_width, new_height2))

    # ウィンドウ終了処理
    window.close()


if __name__ == "__main__":
    show_dialog()
