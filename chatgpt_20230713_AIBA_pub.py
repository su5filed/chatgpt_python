# chat gpt と　Bard との会話
import openai
from tkinter import messagebox, simpledialog, Tk
import PySimpleGUI as sg

import time
import threading
import datetime
from bardapi import Bard

api_key = 'sk-...'
openai.api_key = api_key
logfilename_html = ""
logfilename_txt = ""

# 新しいスレッドで実行する関数
def sleep_thread(seconds):
    time.sleep(seconds)

#chat GPTの応答
def generate_text_chatgpt(count, prompt, conversation_history):
    
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

    # logw("count:("+str(count)+")chatgpt prompt:\n"+prompt)
    logw("CHATGPT", "count:("+str(count)+")chatgpt:\n"+message)
    
    return message

# bardの応答
def generate_text_bard(count, prompt):   
    token = 'xxxxxxxxxxxxxxxxxx'
    bard = Bard(token=token)
    response = bard.get_answer(prompt)['content']
    print(response)

    # logw("count:("+str(count)+")bard prompt:\n"+prompt)
    logw("BARD", "count:("+str(count)+")bard:\n"+response)

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

        if( (event == 'SEND' and len(values) > 0)):
            input_prompt = values['Multiline1']
            count = 0
            logw("HUMAN","--- "+str(count)+" ---")
            logw("HUMAN","count:("+str(count)+")Human:\n"+input_prompt)
            logo("Human:"+ input_prompt)
            generated_text = generate_text_chatgpt(count, input_prompt, conversation_history)
            window['Multiline2'].update(generated_text)
            print("応答 chatgpt:", generated_text)
            logo("応答 chatgpt:"+ generated_text)

            loop_chat(input_prompt, window)

    # ウィンドウ終了処理
    window.close()



def loop_chat(input_prompt,window):
    
    template = "ルール：回答には文章の冒頭にA)を添えて答えて下さい。その後、Q)を添えて相手に質問して下さい。\n"
    # template = ""
    count=1
    conversation_history = []

    # true:ChatGPT自身に問い合わせ、false ChatGptとBardの会話
    chatgpt_to_chatgpt=False
    
    while True:
        logw("NONE", "--- "+str(count)+" ---")
        # Bard に問い合わせ
        if(chatgpt_to_chatgpt == False):
            input_prompt = generate_text_bard(count, input_prompt)
            window['Multiline3'].update(input_prompt)
            print("応答 bard:", input_prompt)
            logo("応答 bard:"+ input_prompt)

        # ChatGPT に問い合わせ
        input_prompt = generate_text_chatgpt(count, template+input_prompt, conversation_history)
        window['Multiline2'].update(input_prompt)
        print("count:",count)
        logo("count:"+ str(count))
        print("応答 chatgpt:", input_prompt)
        logo("応答 chatgpt:"+ input_prompt)

        # 新しいスレッドを作成し、wait()関数を実行する
        t = threading.Thread(target=sleep_thread, args=[13])
        t.start()
        # スレッドがsleepしている間、他の処理を実行する
        print("スレッドがsleepしています")

        # スレッドがsleep状態から解除されるまで待つ
        t.join()
        print("スレッドがsleep状態から解除されました")
        count+=1

        if count > 15:break
    
def logo(line):
    # ログファイルを開きます
    with open(logfilename_txt, 'a') as file:
        # ログを出力します
        file.write(line+'\n')
    # ログファイルをクローズします
    file.close()

def logh(line,logfilename):
    # ログファイルを開きます
    with open(logfilename, 'a') as file:
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
    logh("<tr><td bgcolor="+color+">"+TAG+"</td><td><font color="+color+">"+line+"</font></td>", logfilename_html)        
    
if __name__ == "__main__":
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    logfilename_html = "log_"+timestamp+".html"
    logfilename_txt = "log_"+timestamp+".txt"
    logh("<html><table>", logfilename_html)
    show_dialog()
    logh("</table></html>", logfilename_html)
