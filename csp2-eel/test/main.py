
import eel 
from langchain_community.llms import Ollama
import multiprocessing
import mysql.connector
import json
import subprocess
import re
eel.init("csp home")   

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
   
llm = Ollama(model="autowiz:latest")
queuechatout=[]
import re

def check_for_fill_the_form(input_str):
    keywords = ["fill (out)? (the)? form", "complete form", "form filling", "fill a form", "fill form"]
    pattern = "|".join(keywords)
    if re.search(rf'help.*({pattern})', input_str, re.IGNORECASE):
        return True
    return False

def chatllm(input_str, output_queue):
    k = llm.invoke(input_str)
    k = json.dumps(k)
    k = k[1:-11]
  
    output_queue.put(k)
    
    
@eel.expose
def chatjs(input):
    output_queue = multiprocessing.Queue()
    t = multiprocessing.Process(target=chatllm, args=(input, output_queue))

    t.start()
    t.join()
    
    # Retrieve the value from the queue
    result = output_queue.get()
    queuechatout.append(result)
    print(queuechatout[0])
    return result

if __name__=='__main__':
    eel.start("homepage.html")
    

