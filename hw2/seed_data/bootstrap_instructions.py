import random
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load the OpenAI API key
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"), base_url=os.environ.get("OPENAI_API_BASE")
)


def load_seed_tasks(file_path):
    """Load existing seed tasks from a file."""
    with open(file_path, "r") as file:
        seed_tasks = [json.loads(line) for line in file.readlines()]
    return seed_tasks


def generate_new_task(prompt):
    """Generate a new seed task using OpenAI API."""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content


def save_new_tasks(seed_tasks, file_path):
    """Save the updated list of seed tasks to a file."""
    with open(file_path, "w") as file:
        for task in seed_tasks:
            file.write(json.dumps(task) + "\n")


def is_valid_json(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None


def main():
    seed_tasks = load_seed_tasks("seed_tasks.jsonl")

    while len(seed_tasks) < 250:
        selected_tasks = random.sample(seed_tasks, 8)
        prompt = (
            'Generate a new seed task based on the following instructions and include an example instance. Be sure to keep the format as:\n{"name": "...", "instruction": "...", "instances": [{"input": "...", "output": "..."}], "is_classification": ...}\n'
            + "\n".join([task["instruction"] for task in selected_tasks])
        )

        new_task_description = generate_new_task(prompt)
        if new_task_description is None:
            print("Failed to generate a new task. Please try again.")
            continue
        new_task_description = is_valid_json(new_task_description)
        if new_task_description:
            print(
                f"New task generated successfully: {new_task_description['name']} {len(seed_tasks) - 1}"
            )
        else:
            print(f"Failed to generate a new task at {len(seed_tasks) - 1}")
            continue
        # Assuming new_task_description includes both instruction and instance in one response
        new_id = f"seed_task_{len(seed_tasks)}"
        # add the new_id to the new_task_description
        new_task = {
            "id": new_id,
            "name": new_task_description["name"],
            "instruction": new_task_description["instruction"],
            "instances": new_task_description["instances"],
            "is_classification": new_task_description["is_classification"],
        }
        # add it to the seed_tasks list
        seed_tasks.append(new_task)

    save_new_tasks(seed_tasks, "updated_seed_tasks.jsonl")
    print("New tasks generated and saved successfully.")


if __name__ == "__main__":
    main()
