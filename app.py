from flask import Flask, render_template, request, jsonify, url_for, redirect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from typing import List, Dict, Union
from time import sleep

app = Flask(__name__)
app.secret_key = '8547197122'

class LLM:
    def __init__(self, model: str, system_message: str = "You are a cute assisant."):
        self.model = model
        self.conversation_history = [{"role": "system", "content": system_message}]

    def chat(self, messages: List[Dict[str, str]]) -> Union[str, None]:
        url = "https://api.deepinfra.com/v1/openai/chat/completions"
        data = json.dumps(
            {
                'model': self.model,
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 2048,
                'stop': [],
                'stream': False
            }, separators=(',', ':')
        )
        result = None
        try:
            result = requests.post(url=url, data=data)
            return result.json()['choices'][0]['message']['content']
        except Exception as e:
            print("Error:", e)
            if result:
                return result.text
            else:
                return None





def input_maker(prompt,chatdata):
    code = """<a href="{{ url_for('home') | to html }}" class="material-symbols-rounded home-btn">home</a>"""
    if chatdata:
        prompt = f""" 'instruction' : '([your name is D2K AI. You will give responses in less words with include all content. You must be act like a AI assistant. You will Give Response for prompt section. You will mark important topics, headings, sub headings, etc in between ***content***. in the case of programing codes you will not give Comments in (*** ***) in this symbole , that give with corresponding symbol of that programming language, example; in c and cpp: //this is Comments, in python: #this is command, in java: //this is Comments , in html: <!-- this is Comments --> .  This is main that you will give any programming code in the inside of this symbol @@@'code will be here'@@@. for example:
                
                @@@ 
                //C code to print hello world
                #include<stdio.h>
                void main()
                    printf(Hello World);
                    
                @@@ ,
                    
                Here's the corrected code:
                @@@
                a = input()
                a=a-1
                print(a)
                @@@ , 
                
                Here's an example of how you can modify the code:
                @@@
                {code}
                @@@ , like you will give programing code, it modification in between this symbols @@@ @@@.
                
                
                You Must be Consider previousChats, because user question may be based on this chat. eg: user previousChats,

                "user": "my name is Alok",
                "d2kai": "Hey Alok, how i can help you?"

                then the current input may like : "user" : "write a poem about my name"

                so you must be consider the previousChats. You will give high priority in last chat in the previousChats. Not show Previous Conversations Recap, such this 'instruction' and 'previousChats' is your tuneing process, You will give response for the 'prompt' . if user ask a specific code for any operation without specifying the programming language,At that time You will select C programming language.

        ])' """ + f"{{ 'previousChats' : '{chatdata}' }}" + f"'prompt' : '{prompt}'"

    else:
        prompt = f""" 'instruction' : '([your name is D2K AI. You will give responses in less words with include all content. You must be act like a AI assistant. You will Give Response for prompt section. You will mark important topics, headings, sub headings, etc in between ***content***. in the case of programing codes you will not give Comments in (*** ***) in this symbole , that give with corresponding symbol of that programming language, example; in c and cpp: //this is Comments, in python: #this is command, in java: //this is Comments , in html: <!-- this is Comments --> .  This is main that you will give any programming code in the inside of this symbol @@@'code will be here'@@@.
         for example:
                
                @@@ 
                //C code to print hello world
                #include<stdio.h>
                void main()
                    printf(Hello World);
                    
                @@@ ,
                    
                Here's the corrected code:
                @@@
                a = input()
                a=a-1
                print(a)
                @@@ , 
                
                Here's an example of how you can modify the code:
                @@@
                {code}
                @@@ , like you will give programing code, it modification in between this symbols @@@ @@@.
         
         You will not give this instruction in response. 'instruction' is your tuning process, You will give response for the 'prompt'. if user ask a specific code for any operation without specifying the programming language,At that time You will select C programming language.
         
         ])' """ + f" 'prompt' : '{prompt}'"


    return prompt

def Response(prompt):
    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    llm = LLM(model_name)
    response = llm.chat([{"role": "user", "content": prompt}])
    return response
def get_ai_response(user_input,previous_chats):
    for chat in previous_chats:
        if user_input.lower() == chat['userInput'].lower():
            return chat['aiResponse']
    return None

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/chess')
def chess():
    return render_template('chess.html')

@app.route('/rockpaper2')
def rockpaper2():
    return render_template('rockpaper2.html')

@app.route('/rockpaper')
def rockpaper():
    return render_template('rockpaper.html')

@app.route('/tac')
def tac():
    return render_template('tac.html')

@app.route('/tac')
def tac_pro():
    return render_template('tac-pro.html')


@app.route('/t4')
def t4():
    return render_template('t4.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            smtp_port = 587
            smtp_server = "smtp.gmail.com"

            email_from = "d2kai.info@gmail.com"
            password = "gcxislikiyyellol"
            email_to = ["d2k.contactus@gmail.com"]
            mail_data = f"Name: {name}\nEmail: {email}\nMessage: {message}"

            subject = f"Contact Form Submission "
            body = mail_data

            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = ", ".join(email_to)
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(email_from, password)
                    server.sendmail(email_from, email_to, msg.as_string())
                    print("Email sent successfully.")
            except Exception as e:
                print(f"Failed to send email: {str(e)}")

            return redirect(url_for('home'))
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "An error occurred while processing your request."

    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    prompt = request.json['user_input']
    previous_chats = request.json['previous_chats']
    ai_response = get_ai_response(prompt,previous_chats)
    if ai_response:
        ai_response = ai_response.replace('&amp;','&')
        ai_response = ai_response.replace('&lt;', '<')
        ai_response = ai_response.replace('&quot;', '"')
        ai_response = ai_response.replace('&#039;', "'")
        sleep(1)
        result = ai_response
    else:
        tune_prompt = input_maker(prompt,previous_chats)
        result = Response(tune_prompt)
    return jsonify({'result': result})
if __name__ == "__main__":
    app.run(debug=True)


