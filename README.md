# ParseMind

ParseMind is an LLM-powered tool that parses and summarizes newsletters into clean, concise insights.

![alt text](pics/chris-blonk-swd3FBSEA4Q-unsplash.jpg)

Photo by [Chris Blonk](https://unsplash.com/@chriskristiansen?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/six-black-wooden-frames-swd3FBSEA4Q?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
      

## Install

Download `credentials.json` to access the Gmail API following [these instructions](https://developers.google.com/workspace/gmail/api/quickstart/python) and place it under the folder `credentials`.

pip install `parsemind`:
```shell
make install
```

Generate the authorization token:
```shell
python scripts/authorize_and_save_token.py
```


## Requirements

You need to have [ollama](https://ollama.com/) installed.

For MacOS:
```
brew install ollama
```

Also, you need to have downloaded `Ollama.app` from [here](https://ollama.com/download).

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
