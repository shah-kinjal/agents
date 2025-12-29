from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from anthropic import Anthropic
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Kinjal Shah"
        reader = PdfReader("me/LinkedIn-Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        reader = PdfReader("me/KinjalShah_Resume.pdf")
        self.resume = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("me/ks_summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
       
        

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"I would like you to act as a Senior Human Resources professional with 20 years of Human Resources experience. \
        You are an expert at reviewing resumes, selecting the best candidates for interviews, and deciding who to hire. Your career experience has \
        made you a recognized expert in the field of Human Resources at using Applicant Tracking Systems like Workday, BambooHR, Taleo, iCIMS, and \
        others to select the best resumes that have been submitted and filter out applicants who do not meet the requirements for the job. I am \
        going to provide you with the web link of a job description and I would like you to please provide me with the three most important \
        responsibilities in the job description and the five most important key words or phrases an applicant tracking system will be \
        looking for in resumes. \
        I would like you to please help me tailor my resume to the job description based on the three most important responsibilities \
        and the top five key words that you noted. In addition, if there are changes you believe would make my resume a stronger fit,\
        please also make those changes. Please keep my resume lenght to minimun 1 and half pages to maximum 2 pages. \
        Here is the text of my current resume as well as my linked in profile: "
        system_prompt += f"\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please tailor the resume everytime a new job description link is provided. "
        system_prompt += f"finally, I would like you to output final new full version of my resume."
        #return system_prompt
        return 'temp'
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        print (messages)
        response = self.callDeepseek(self, messages)
        return response.choices[0].message.content
    
    def callDeepseek(self, messages):
        deepseek = OpenAI(api_key=self.deepseek_api_key, base_url="https://api.deepseek.com/v1")
        model_name = "deepseek-chat"    
        answer = deepseek.chat.completions.create(
            model=model_name,
            messages=messages,
            base_url='https://api.deepseek.com/v1'
        )
        return answer
    def callOpenAI(self, messages):
        answer = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return answer
    
    def callGroq(self, messages):
        groq=OpenAI(base_url='https://api.groq.com/openai/v1',api_key=self.groq_api_key)
        model_name="llama3-70b-8192"
        answer = groq.chat.completions.create(
            model=model_name,
            messages=[{'role': 'user', 'content': messages}],
            base_url="https://api.groq.com/openai/v1"
        )
        return answer
    
    def callanthropic(self, messages):
        anthropic = Anthropic(api_key=self.anthropic_api_key)
        model_name = "claude-3-5-sonnet-20240620"
        answer = anthropic.messages.create(
                model=model_name,
                messages=[{'role': 'user', 'content': messages}],
                max_tokens=1000
            ).content[0].text
        return answer
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    