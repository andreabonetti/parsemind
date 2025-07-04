# NOTE: you need to:
# - install in ollama the models that you need, like gemma3:1b
# - run `ollama serve` first in the terminal

from parsemind import ollama

model = 'gemma3:4b'
prompt = 'Hi there!'
response = ollama(prompt=prompt, model=model)

print('')
print(f"**Prompt:**\n{prompt}")
print('')
print(f"**LLM:**\n{response}")
print('')
