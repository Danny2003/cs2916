import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# OpenAI API key
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
	base_url=os.environ.get("OPENAI_API_BASE")
)

# Example seed task in json
with open('seed_tasks.jsonl', 'r') as file:
	seed_task = json.loads(file.readlines()[0])

# Function to generate new instances
def generate_instances(task, n=4):
	if task['is_classification']:
		prompt = f"Here is a classification task named \"{task['name']}\", the instruction of the classification task is:\n{task['instruction']}\nFor example, when the input is:\n{task['instances'][0]['input']}\nthe output is:\n{task['instances'][0]['output']}\nGenerate {n} new pairs of input and output, be sure to keep the format the same as [{{\"input\": \"the content of new input\", \"output\": \"the content of new output\"}}, ...]\nTry to balance the number of different classes in the {n} new pairs."
		response = client.chat.completions.create(
			messages=[
				{
					"role": "user",
					"content": prompt,
				}
			],
			model="gpt-3.5-turbo",
		)
		if  response.choices[0].message.content is not None:
			return json.loads(response.choices[0].message.content)
	elif task['instances'][0]['input'] != "":
		print(f"{task['id']}: {task['name']} has input.\n")
		prompt = f"Here is a task named \"{task['name']}\", the instruction of the task is:\n{task['instruction']}\nFor example, when the input is:\n{task['instances'][0]['input']}\nthe output is:\n{task['instances'][0]['output']}\nGenerate {n} new pairs of input and output, be sure to keep the format the same as [{{\"input\": \"the content of new input\", \"output\": \"the content of new output\"}}, ...]"
		response = client.chat.completions.create(
			messages=[
				{
					"role": "user",
					"content": prompt,
				}
			],
			model="gpt-3.5-turbo",
		)
		if  response.choices[0].message.content is not None:
			return json.loads(response.choices[0].message.content)
	else:
		print(f"{task['id']}: {task['name']} has no input.\n")
		prompt = f"Here is a task named \"{task['name']}\", the instruction of the task is:\n{task['instruction']}\nFor example, the output is:\n{task['instances'][0]['output']}\nGenerate {n} new pairs of input and output, since this is a task that doesn't have an input, be sure to keep the format the same as [{{\"input\": \"\", \"output\": \"the content of new output\"}}, ...], where the input should be an empty string and the output should be a non-empty string."
		response = client.chat.completions.create(
			messages=[
				{
					"role": "user",
					"content": prompt,
				}
			],
			model="gpt-3.5-turbo",
		)
		if  response.choices[0].message.content is not None:
			return json.loads(response.choices[0].message.content)

# Generate a new instance and print it
new_instance = generate_instances(seed_task)
seed_task['instances'].extend(new_instance)
with open('expanded_seed_tasks.jsonl', 'w') as file:
	file.write(json.dumps(seed_task) + '\n')
