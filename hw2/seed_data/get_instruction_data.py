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

# Load existing seed tasks
with open('seed_tasks.jsonl', 'r') as file:
    seed_tasks = [json.loads(line) for line in file.readlines()]

# Function to generate additional instances using OpenAI's GPT-3.5
def generate_instances(task, n=4):
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

# Add new instances to each task
new_tasks = []
for task in seed_tasks:
	if len(new_tasks) < 250:
		new_instances = generate_instances(task)
		task['instances'].extend(new_instances)
		new_tasks.append(task)

# Save the expanded tasks back to a new JSONL file
with open('expanded_seed_tasks.jsonl', 'w') as file:
	for task in new_tasks:
		file.write(json.dumps(task) + '\n')

print(f"Generated and saved expanded tasks with a total of {len(new_tasks)} tasks.")
