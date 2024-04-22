# Instruction generation

## Setup the API key

Create a file `.env` and input the following lines:

```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
OPENAI_API_BASE="YOUR_OPENAI_API_BASE"
```

## Install the requirements

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Seed task expansion

Expand the seed tasks to 250 tasks. The seed tasks are in `seed_tasks.jsonl`. The expanded tasks will be in `expanded_tasks.jsonl`.

```bash
python bootstrap_instructions.py
```

## Instance generation

Generate the instances for `expanded_tasks.jsonl`. The output file `updated_seed_tasks.jsonl` will contain all the instances (at least 5).

```bash
python generate_instances.py
```
