# ParseMind
ParseMind is an LLM-powered tool that parses and summarizes newsletters into clean, concise insights.

## Install

Download `credentials.json` to access the Gmail API following [these instructions](https://developers.google.com/workspace/gmail/api/quickstart/python) and place it under the folder `credentials`.

pip install `parsemind`:
```shell
make install
```

Generate the authorization token:
```
python scripts/authorize_and_save_token.py
```


## Requirements

You need to have [ollama](https://ollama.com/) installed.

## How to use it

Start ollama:
```shell
ollama serve
```

Run any of the available scripts (or create your own):
```shell
python scripts/generate_summary_collection.py
```

## Documentation
- [todo](documentation/todo.md)
