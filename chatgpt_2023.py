# PythonからGPT-4を使用するためにはOpenAIのパッケージを最新版にしておく必要があります。
# 以下のコマンドで、現時点で最新版のパッケージに更新します。

import openai
from tkinter import messagebox, simpledialog, Tk
import PySimpleGUI as sg

api_key = 'sk-....'
openai.api_key = api_key

def generate_text(prompt, conversation_history):
    # プロンプトを会話履歴に追加
    conversation_history.append({"role": "user", "content": prompt})

    # GPT-4モデルを使用する場合
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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


def show_dialog():
    # ウィンドウのテーマ
    sg.theme('BlueMono')

    width = 600
    height = 20

    # ウィンドウのレイアウト
    layout = [
            [sg.Button('SEND', size=(10, 1), key='SEND'),sg.Button('CLOSE', size=(10, 1), key='CLOSE') ],
            [sg.Multiline(default_text="", size=(width,5)) ],
            [sg.Multiline(default_text="", size=(width,10), key='Multiline2') ],
        ]

    # ウィンドウオブジェクトの作成
    window = sg.Window('title', layout, size=(700, 300))

    # 会話履歴を格納するためのリストを初期化
    conversation_history = []

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

        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break
        
        if len(values) > 0 :
            input_prompt = values[0]
            generated_text = generate_text(input_prompt, conversation_history)
            window['Multiline2'].update(generated_text)
            print("応答:", generated_text)

    # ウィンドウ終了処理
    window.close()

if __name__ == "__main__":
    show_dialog()

        
