"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyBMvepv-_OgN2A8CGn5MwwHRH3_aBWgyXs")

# Set up the model
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
        print('hi')
    except Exception as e:
        print("An error occurred while executing the code:", e)





model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings,tools=[execute_python_code])

convo = model.start_chat(enable_automatic_function_calling=True)

convo.send_message("What is product of  2 and 2")
print(convo.last.text)