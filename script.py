import requests
import json

url = "http://localhost:11434/api/generate"

transcript_file = open("data/transcript.txt", "r",encoding="utf8")
transcript = transcript_file.read()
transcript_file.close()

headers = {
    'Content-Type': 'application/json'
}

# Extract Functional Requirements from Meeting Transcript
prompt1 = "Analyze the following meeting transcript and list all functional requirements mentioned. Focus on features, user actions, and system behaviors. " + transcript
# Extract Non-Functional Requirements from Meeting Transcript
prompt2 = "From the transcript, extract all non-functional requirements such as performance, scalability, security, and usability. List any constraints or quality attributes mentioned in the meeting. " + transcript
# Identify User Stories from Meeting Transcript
prompt3 = "Convert the requirements in this transcript into user stories. Use the format: 'As a [user role], I want [feature] so that [benefit]. Prioritize them based on importance. " + transcript
# Summarize requirements
prompt4 = "Summarize the software requirements discussed in this meeting. Include functional, non-functional, and constraints. Provide a concise summary. " + transcript
# Clarify Ambiguities
prompt5 = "Identify any ambiguous statements in the transcript and suggest clarifying questions to resolve them. " + transcript


print("Welcome to the Requirements Analysis Tool!")
print("Please select an option:")
print("1. Extract Functional Requirements")
print("2. Extract Non-Functional Requirements")
print("3. Identify User Stories")   
print("4. Summarize Requirements")
print("5. Clarify Ambiguities")
choice = input("Enter your choice (1-5): ")

if choice == "1":
    prompt = prompt1
elif choice == "2":
    prompt = prompt2
elif choice == "3":
    prompt = prompt3
elif choice == "4":
    prompt = prompt4
elif choice == "5":
    prompt = prompt5
else:
    print("Invalid choice. Please enter a number between 1 and 5.")
    exit()

initial_prompt = prompt
initial_response = ""

data = {
    "model": "llama3.2",#"deepseek-r1:8b", #"llama3.2", # Change to the model you want to use
    "prompt": prompt, 
    "options": {
        "num_ctx": 8192 
    },
    "stream": False,
}

def handle_comments():
    global data, initial_prompt, initial_response
    
    print("Would you like to add any comments to the generated text?")
    print("1. Yes")
    print("2. No")  
    choice = input("Enter your choice (1-2): ")
    if choice == "1":
        comment = input("Enter your comment: ")        
        data = {
            "model": "llama3.2",#"deepseek-r1:8b", #"llama3.2", # Change to the model you want to use
            "prompt": f"{initial_prompt}\n{initial_response}\n{comment}", 
            "options": {
                "num_ctx": 8192 
            },
            "stream": False,
        }
        print("Thank you for your feedback!")
        generate_text()
    elif choice == "2":
        print("Thank you for using the Requirements Analysis Tool!")
    else:
        print("Invalid choice. Please enter a number between 1 and 2.")
        exit()

def generate_text():
    global data, initial_response

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        if initial_response == "":
            initial_response = actual_response
        print(actual_response)
        handle_comments()
    else:
        print("Error:", response.status_code, response.text)

generate_text()