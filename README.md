# provingPython(wip)
Definitions, theorems and proofs written in Python. You can verify these proofs with [Pyright](https://github.com/microsoft/pyright). Please note that you cannot use mypy as it passes invalid proofs.
## Usage
### Visual Studio Code
Install [Pylance plugin](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) and set type checking mode to "basic" at Settings > Python > Type Cheking Mode. Then, open proof files and if you don't see any type error, proofs are correct.
### Command Line
Install [Pyright](https://github.com/microsoft/pyright) and run type check on proof files.
```console
$ pip install pyright
$ pyright proposition.py
No configuration file found.
No pyproject.toml file found.
stubPath /Users/kaicho8636/Projects/provingPython/typings is not a valid directory.
Assuming Python platform Darwin
Searching for source files
Found 1 source file
pyright 1.1.267
0 errors, 0 warnings, 0 informations 
Completed in 0.97sec
```
