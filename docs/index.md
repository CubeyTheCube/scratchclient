# Scratchclient Documentation

This is the documentation for scratchclient.

## Installation

Go to your terminal (not your python shell) and execute this command:
```bash
pip install scratchclient
```

If this didn't work for whatever reason, open your python shell and run the following:
```python
import os; os.system("pip install scratchclient")
```

scratchclient requires Python 3.7; however, it will work for almost all use cases on Python 3.6.

## Get Started
```python
from scratchclient import ScratchSession

session = ScratchSession("ceebee", "--uwu--")

# post comments
session.get_user("Paddle2See").post_comment("OwO")

# lots of other stuff
print(session.get_project(450216269).get_comments()[0].content)
print(session.get_studio(29251822).description)
```

## Cloud Connection
```python
from scratchclient import ScratchSession

session = ScratchSession("griffpatch", "SecurePassword7")

connection = session.create_cloud_connection(450216269)

connection.set_cloud_variable("variable name", 5000)

@connection.on("set")
def on_set(variable):
    print(variable.name, variable.value)

print(connection.get_cloud_variable("other variable"))
```

See the examples for more code samples.

## CLI

scratchclient has a command line interface for retrieving Scratch website data from the command line. Use `python3 -m scratchclient help` to get started.