# chat gpt と　Bard との会話
import openai
from tkinter import messagebox, simpledialog, Tk
import PySimpleGUI as sg

import time
import threading
import datetime
import os
from bardapi import Bard

api_key = 'sk-...'
openai.api_key = api_key
folder = 'log'
logfilename_html = ""
logfilename_txt = ""
threading_pub = None

# 新しいスレッドで実行する関数
def sleep_thread(seconds,input_prompt, window, checkbox1_value, loop_count, InputText_template):
    loop_chat(input_prompt, window, checkbox1_value, loop_count, InputText_template)

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
            [sg.Button('SEND', size=(10, 1), key='SEND'),sg.Button('STOP', size=(10, 1), key='STOP'),sg.Button('CLEAR', size=(10, 1), key='CLEAR'),sg.Button('CLOSE', size=(10, 1), key='CLOSE'),sg.Checkbox('ChatGptのみの自問自答', key='Checkbox1'),
             sg.Text('回数：', size=(4, 1), key='Question'),sg.InputText('15', size=(10, 1), key='InputText') ],
            [sg.InputText('ルール：回答には文章の冒頭にA)を添えて答えて下さい。その後、Q)を添えて相手に質問して下さい。', size=(initial_width, 1), key='InputText_template') ],
            [sg.Multiline(default_text="", size=(initial_width,5),  key='Multiline1') ],
            [sg.Multiline(default_text="", size=(initial_width,10), key='Multiline2') ],
            [sg.Multiline(default_text="", size=(initial_width,10), key='Multiline3') ],
        ]

    # ウィンドウオブジェクトの作成
    window = sg.Window('title', layout, size=(700, 480), resizable=True)

    logh("<html><table>", logfilename_html)

    # イベントのループ
    while True:
        # イベントの読み込み
        event, values = window.read()
        # 変更部分
        print('Event: ', event)
        print('values: ', values)
        
        # 変更部分終わり
        if event == 'CLOSE':
            logh("</table></html>", logfilename_html)
            break

        if event == 'CLEAR':
            window['Multiline1'].update("")

        if event == 'STOP':
            # 一定の時間後にスレッドを中断する
            if threading_pub != None:
                threading_pub.interrupted = True
            # 押せるようにする
            window['SEND'].update(disabled=False)
        
        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break

        if( (event == 'SEND' and len(values) > 0)):
            loop_count = values['InputText']
            if loop_count.isnumeric() == False:
                sg.popup('入力は数字ではありません')
            else:
                input_prompt = values['Multiline1']
                count = 0
                logw("HUMAN","--- "+str(count)+" ---")
                logw("HUMAN","count:("+str(count)+")Human:\n"+input_prompt)
                logo("Human:"+ input_prompt)
                
                checkbox1_value = values['Checkbox1']
                InputText_template = values['InputText_template']

                # 押せないようにする
                window['SEND'].update(disabled=True)
                # 新しいスレッドを作成し、wait()関数を実行する
                threading_pub = threading.Thread(target=sleep_thread, args=[30,input_prompt, window, checkbox1_value, int(loop_count), InputText_template])
                threading_pub.interrupted = False
                threading_pub.start()
            

    # ウィンドウ終了処理
    window.close()

# Q)以降を切り出して、相手に質問する。
def cut_question(input_prompt):
    search_keyword="Q)"
    if search_keyword in input_prompt:
        # print("before:",input_prompt)
        index = input_prompt.index(search_keyword) #+ len(search_keyword)
        input_prompt = input_prompt[index:]
        # print(" after:",input_prompt)
    return input_prompt

def loop_chat(input_prompt,window, checkbox1_value, loop_count, InputText_template):
    
    # template = "ルール：回答には文章の冒頭にA)を添えて答えて下さい。その後、Q)を添えて相手に質問して下さい。\n"
    # template = "応答する際に、何か質問を添えて下さい。\n"
    template = InputText_template
    count=1
    
    # true:ChatGPT自身に問い合わせ、false ChatGptとBardの会話
    chatgpt_to_chatgpt = checkbox1_value

    # 回数が０以下の場合
    if loop_count < 1:
        loop_count = 1

    while True:
        # スレッドが中断された場合はループを抜ける
        if threading.current_thread().interrupted:
            print("stop thread.")
            break
        
        logw("NONE", "--- "+str(count)+" ---")

        # ChatGPT に問い合わせ
        conversation_history = []
        input_prompt = generate_text_chatgpt(count, template+cut_question(input_prompt), conversation_history)
        window['Multiline2'].update(input_prompt)
        print("count:",count)
        logo("count:"+ str(count))
        print("応答 chatgpt:", input_prompt)
        logo("応答 chatgpt:"+ input_prompt)
        time.sleep(10)

        # スレッドが中断された場合はループを抜ける
        if threading.current_thread().interrupted:
            print("stop thread.")
            break
    
        # Bard に問い合わせ
        conversation_history = []
        if(chatgpt_to_chatgpt == False):
            input_prompt = generate_text_bard(count, template+cut_question(input_prompt))
            window['Multiline3'].update(input_prompt)
            print("応答 bard:", input_prompt)
            logo("応答 bard:"+ input_prompt)
            time.sleep(10)
        
        
        count+=1

        if count > loop_count:
            print("loop end")
            # 押せるようにする
            window['SEND'].update(disabled=False)
            break
    
def logo(line):
    # ログファイルを開きます
    with open(logfilename_txt, 'a') as file:
        # ログを出力します
        file.write(line+'\n')
    # ログファイルをクローズします
    file.close()

def logh(line,logfilename):
    line.encode("utf-8")
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

    if not os.path.exists(folder):
        os.makedirs(folder)
    
    logfilename_html = "log/AI_"+timestamp+".html"
    logfilename_txt = "log/AI_"+timestamp+".txt"

    show_dialog()
