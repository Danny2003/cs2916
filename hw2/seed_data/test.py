import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# OpenAI API key
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Example seed task in json
with open('seed_tasks.jsonl', 'r') as file:
	seed_task = json.loads(file.readlines()[0])

# Function to generate a new instance
def generate_instance(task, n=1):
	if ("task['instances'][0]['input']" != ""):
		prompt = f"Here is a task named \"{task['name']}\", the instruction of the task is:\n{task['instruction']}\nFor example, when the input is:\n{task['instances'][0]['input']}\nthe output is:\n{task['instances'][0]['output']}\nGenerate a new pair of input and output, be sure to keep the format the same as {{\"input\": \"the content of new input\", \"output\": \"the content of new output\"}}"
		response = client.chat.completions.create(
			messages=prompt,
			model="gpt-3.5-turbo",
		)
		return [{"input": instance['input'], "output": instance['output']} for instance in response.choices]
	else:
		prompt = f"Here is a task named \"{task['name']}\", the instruction of the task is:\n{task['instruction']}\nFor example, the output is:\n{task['instances'][0]['output']}\nGenerate a new output, since this is a task that doesn't have an input, be sure to keep the format the same as {{\"input\": \"\", \"output\": \"the content of new output\"}}"
		response = client.chat.completions.create(
			messages=prompt,
			model="gpt-3.5-turbo",
		)
		return [{"input": instance['input'], "output": instance['output']} for instance in response.choices]

# Generate a new instance and print it
new_instance = generate_instance(seed_task)
seed_task['instances'].extend(new_instance)
with open('expanded_seed_tasks.jsonl', 'w') as file:
	file.write(json.dumps(seed_task) + '\n')
