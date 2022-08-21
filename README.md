# provingPython
Definitions, theorems and proofs written in Python. You can verify these proof with [Pyright](https://github.com/microsoft/pyright).
## Usage
### Visual Studio Code
Install [Pylance plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) and set type checking mode to "basic" at Settings > Python > Type Cheking Mode. Then, open proof files and if you don't see any type error, proofs are correct.
### Command Line
Install [Pyright](https://github.com/microsoft/pyright) and run type check on proof files.
```console
$ pip install pyright
$ pyright proposition.py
```
