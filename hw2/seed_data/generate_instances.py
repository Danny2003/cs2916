import os
from openai import OpenAI
import json
from dotenv import load_dotenv

# OpenAI API key
load_dotenv()
client = OpenAI(
	# This is the default and can be omitted
	api_key=os.environ.get("OPENAI_API_KEY"),
	base_url=os.environ.get("OPENAI_API_BASE"),
)

# Load existing seed tasks
with open("updated_seed_tasks.jsonl", "r") as file:
	seed_tasks = [json.loads(line) for line in file.readlines()]


def is_valid_json(s):
	try:
		return json.loads(s)
	except json.JSONDecodeError:
		return None


# Function to generate new instances
def generate_instances(task, n=4):
	if n > 0:
		if task["is_classification"]:
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
			if response.choices[0].message.content:
				return is_valid_json(response.choices[0].message.content)
		elif task["instances"][0]["input"] != "":
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
			if response.choices[0].message.content:
				return is_valid_json(response.choices[0].message.content)
		else:
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
			if response.choices[0].message.content:
				return is_valid_json(response.choices[0].message.content)
	else:
		return None


# Add new instances to each task
new_tasks = []
failed_tasks = []
for task in seed_tasks:
	i = 0
	while len(task["instances"]) < 5:
		new_instances = generate_instances(task, max(0, 5 - len(task["instances"])))
		if new_instances:
			task["instances"].extend(new_instances)
		i += 1
		if i > 10:
			failed_tasks.append(task)
			print(f"Failed to generate new instances for task {task['id']}.")
			break

	new_tasks.append(task)
	num=len(task["instances"])
	print(f"Successfully generated {num} instances for task {task['id']}.")

# Save the expanded tasks back to a new JSONL file
with open("expanded_seed_tasks.jsonl", "w") as file:
	for task in new_tasks:
		file.write(json.dumps(task) + "\n")

if failed_tasks:
	with open("failed_tasks.jsonl", "w") as file:
		for task in failed_tasks:
			file.write(json.dumps(task) + "\n")

print(f"Generated and saved expanded tasks with a total of {len(new_tasks)} tasks.\n")
