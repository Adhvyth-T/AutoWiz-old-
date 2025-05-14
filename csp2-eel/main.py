
import eel 

import ast
import multiprocessing
import mysql.connector
import json
eel.init("csp home")   
import google.generativeai as genai
import google.ai.generativelanguage as glm
import subprocess
eel.init("csp home")
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}
safety_settings = [

  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  }
]
def execute_python_code(code_string:str):
    try:
        
        exec(code_string)
    except Exception as e:
        print("An error occurred while executing the code:", e)
execute_pythonCode = glm.Tool(
    function_declarations=[
      glm.FunctionDeclaration(
        name='execute_python_code',
        description="executes the python script passed as string into it",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'code_string':glm.Schema(type=glm.Type.STRING)
                
            },
            required=['code_string']
        )
      )
    ])
glm.Tool(execute_pythonCode)

def fileconversion():
    subprocess.run(["python", "fileconv.py"])

def formfiller():
    subprocess.run(["python", "formfiller.py"])



genai.configure(api_key="AIzaSyBMvepv-_OgN2A8CGn5MwwHRH3_aBWgyXs")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings,tools=[execute_python_code,fileconversion,formfiller])
system_instruction = "don't use emojis in response"
convo = model.start_chat(enable_automatic_function_calling=True)
db= mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="batman3",
  database="csp2"
)
cursor = db.cursor()


@eel.expose
def handle_messages(date, user_messages, ai_messages):
    user_messages = json.loads(user_messages)
    ai_messages = json.loads(ai_messages)
   
    # Open a cursor to perform database operations
 
    print(date)
    print("Incoming Messages:")
    for msg in user_messages:
        print(msg['text'])

    print("Outgoing Messages:")
    for msg in ai_messages:
        print(msg['text'])
    chatName=user_messages[0]['text'][:10]
    # Insert user and AI messages into the database
    cursor.execute(
        "INSERT INTO chat_history (chat_date,chat_name, user_chat, ai_chat) VALUES (%s,%s, %s, %s)",
        (date,chatName, json.dumps(user_messages), json.dumps(ai_messages))
    )
    # Commit the transaction
    db.commit()
@eel.expose
def getChathist():
    cursor.execute(
        "SELECT chat_name,chat_date FROM chat_history"
    )
    row=cursor.fetchall()
    for i in row:
        cn=i[0]
        cd=i[1]
        eel.ChathistInsert(cn,cd)
    
@eel.expose
def fetch_chat_rows():
    # Open a cursor to perform database operations
    cursor = db.cursor()

    # Fetch "user_chat" and "ai_chat" rows from the MySQL table
    cursor.execute("SELECT user_chat, ai_chat FROM chat_history")
    rows = cursor.fetchall()

    # Convert fetched data into a list of dictionaries
    chat_data = [{'user_chat': json.loads(row[0]), 'ai_chat': json.loads(row[1])} for row in rows]

    # Close the cursor
    

    # Return data as JSON string
    return json.dumps(chat_data)
   
queuechatout=[]



def chatllm(input_str, output_queue):
    convo.send_message(input_str)
    
   
    k=ast.literal_eval(json.dumps(convo.last.text))
    
    encoded_str = k.encode('utf-8', errors='ignore')
    
    # Decode the UTF-8 encoded string
    decoded_str = encoded_str.decode('utf-8')
  
    output_queue.put(decoded_str)

   
    
@eel.expose
def chatjs(input):
    output_queue = multiprocessing.Queue()
    t = multiprocessing.Process(target=chatllm, args=(input, output_queue))

    t.start()
    t.join()
    
    # Retrieve the value from the queue
    result = output_queue.get()
    queuechatout.append(result)
    print(queuechatout[-1])
    return result

if __name__=='__main__':
    eel.start("homepage.html")
    

