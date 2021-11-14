# scratchclient
A scratch API wrapper for python. 

Based off of https://github.com/edqx/node-scratch-client, and [ilcheese2](https://scratch.mit.edu/users/ilcheese2/)'s cloud code based on my own. 

## Installation

Go to your terminal (not your python shell) and execute this command:
```bash
pip install scratchclient
```

If you want cloud variables to run faster, use this command:
```bash
pip install scratchclient[fast]
```
Note that to do this, you need to install [Visual C++ 14.0](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## Example usage

### Basic usage:
```python
from scratchclient import ScratchSession

session = ScratchSession("ceebee", "--uwu--")

# post comments
session.get_user("Paddle2See").post_comment("OwO")

# lots of other stuff
print(session.get_project(450216269).get_comments()[0].content)
print(session.get_studio(29251822).description)
```
### Cloud connection:
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

Documentation is on the way.

All bugs should be reported to the [github repository](https://github.com/CubeyTheCube/scratchclient) or my [Scratch profile](https://scratch.mit.edu/users/Raihan142857/).
