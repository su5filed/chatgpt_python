# chat gpt と　Bard
import openai
from tkinter import messagebox, simpledialog, Tk
import PySimpleGUI as sg

from bardapi import Bard


import time
import threading
import datetime
import os

api_key = 'sk-.....'
openai.api_key = api_key

folder = 'log'

logfilename_html = ""
logfilename_txt = ""

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

    logh("<html><table>")

    # イベントのループ
    while True:
        # イベントの読み込み
        event, values = window.read()
        # 変更部分
        print('Event: ', event)
        print('values: ', values)
        
        # 変更部分終わり
        if event == 'CLOSE':
            logh("</table></html>")
            break

        if event == 'CLEAR':
            window['Multiline1'].update("")

        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break
        
        if( event == 'SEND' and len(values) > 0 ):
            
            input_prompt = values['Multiline1']

            # 新しいスレッドを作成し、wait()関数を実行する
            t = threading.Thread(target=sleep_thread, args=[30,input_prompt,window])
            t.start()
            # スレッドがsleepしている間、他の処理を実行する
            print("スレッドがsleepしています")
            # スレッドがsleep状態から解除されるまで待つ
            # t.join()
            print("スレッドがsleep状態から解除されました")

        
    # ウィンドウ終了処理
    window.close()


# 新しいスレッドで実行する関数
def sleep_thread(seconds,input_prompt,window):
    # 会話履歴を格納するためのリストを初期化
    # time.sleep(seconds)
    conversation_history = []
    conversation_history_bard = []
    # 押せないようにする
    window['SEND'].update(disabled=True)
    logw("HUMAN", input_prompt)
    generated_text = generate_text_chatgpt(input_prompt, conversation_history)
    window['Multiline2'].update(generated_text)
    print("応答 chatgpt:", generated_text)
    logw("CHATGPT", generated_text)
    generated_text = generate_text_bard(input_prompt, conversation_history_bard)
    window['Multiline3'].update(generated_text)
    print("応答 bard:", generated_text)
    logw("BARD", generated_text)
    # 押せるようにする
    window['SEND'].update(disabled=False)


def logh(line):
    # ログファイルを開きます
    with open(logfilename_html, 'a') as file:
        # ログを出力します
        file.write(line+'\n')
    # ログファイルをクローズします
    file.close()

def logw(TAG, line):
    color="black"
    if TAG=="BARD":
        color="blue"
    elif TAG=="CHATGPT":
        color="red"
    elif TAG=="HUMAN":
        color="green"
    logh("<tr><td bgcolor="+color+">"+TAG+"</td><td><font color="+color+"><pre>"+line+"</pre></font></td>")        
    


if __name__ == "__main__":
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    logfilename_html = "log/log_"+timestamp+".html"

    show_dialog()
