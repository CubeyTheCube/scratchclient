# CloudConnection

## Properties

###`#!python project_id : int` { #project_id data-toc-label="project_id" }

The ID of the project that the connection is on.

###`#!python cloud_host : str` { #cloud_host data-toc-label="cloud_host" }

The hostname of the server where the cloud variables are hosted.

## Methods

###`#!python run()` { #run data-toc-label="run" }

Connects to the server and starts listening for variable changes.

**Example:**

```python
connection = session.create_cloud_connection(193290310931, is_async=True)

@connection.on("connect")
async def on_connect():
    print("Connected!")

@connection.on("set")
async def on_set(variable):
    print(variable.name, variable.value)

connection.run()
```

###`#!python await connect()` { #connect data-toc-label="connect" }

Connects to the server and starts listening for variable changes. Equivalent to [AsyncCloudConnection.run](#run) except it's a coroutine. Must be called with `#!python await`.

###`#!python get_cloud_variable(name)` { #get_cloud_variable data-toc-label="get_cloud_variable" }

Gets the value of a cloud variable with the specified name.

**PARAMETERS**

- **name** (`#!python str`) - The name of the variable.  The name does not necessarily need to include the cloud emoji ("☁️ ").

**RETURNS** - `#!python str`

**Example:**

```python
connection = session.create_cloud_connection(193290310931, is_async=True)

@connection.on("connect")
async def on_connect():
    print(connection.get_cloud_variable("High score"))
    # 102930921

connection.run()
```

###`#!python await set_cloud_variable(name, value)` { #set_cloud_variable data-toc-label="set_cloud_variable" }

Sets the value of a cloud variable with the specified name to the specified value. You can only do this 10 times per second. This function must be used with `#!python await`.

**PARAMETERS**

- **name** (`#!python str`) - The name of the variable.  The name does not necessarily need to include the cloud emoji ("☁️ ").
- **value** (`#!python str`) - The value you want to set the cloud variable to. This must be less than 256 characters long and all digits.

**Example:**

```python
connection = session.create_cloud_connection(193290310931, is_async=True)

@connection.on("connect")
async def on_connect():
    await connection.set_cloud_variable("High score", 102930921)
    print(connection.get_cloud_variable("High score"))
    # 102930921

connection.run()
```

###`#!python await create_cloud_variable(name, initial_value=0)` { #create_cloud_variable data-toc-label="create_cloud_variable" }

Creates a cloud variable with the specified name and sets it to the specified initial value. You can only do this 10 times per second. This function must be used with `#!python await`.

**PARAMETERS**

- **name** (`#!python str`) - The name of the new variable.  The name does not necessarily need to include the cloud emoji ("☁️ ").
- **initial_value** (`#!python int`) - The value you want to set the cloud variable to. This must be less than 256 characters long and all digits.

**Example:**

```python
connection = session.create_cloud_connection(193290310931, is_async=True)

@connection.on("connect")
async def on_connect():
    await connection.create_cloud_variable("High score", 10)

connection.run()
```

!!! note
    This will not update live for other people using the project.

###`#!python await delete_cloud_variable(name)` { #delete_cloud_variable data-toc-label="delete_cloud_variable" }

Deletes a cloud variable with the specified name. You can only do this 10 times per second. This function must be used with `#!python await`.

**PARAMETERS**

- **name** (`#!python str`) - The name of the variable to be deleted.  The name does not necessarily need to include the cloud emoji ("☁️ ").

**Example:**

```python
connection = session.create_cloud_connection(193290310931, is_async=True)

@connection.on("connect")
def on_connect():
    await connection.delete_cloud_variable("High score")

connection.run()
```

!!! note
    This will not update live for other people using the project.

###`#!python on(key, callback=None, once=False)` { #on data-toc-label="on" }

Adds an event for the connection listen to. This can either be used as a decorator or a function.

**PARAMETERS**

- **key** (`#!python str`) - The key of the event to be listened to.
- **callback** (`#!python callable`) - The function that will run when the event occurs.
- **once** (`#!python bool`) - Whether the event should only be fired once.

**RETURNS** - `#!python None | callable`

**Example:**

```python
# Use as a function
async def on_set(variable):
    print(variable.name, variable.value)

connection.on("set", on_set)

# Use as a decorator
@connection.on("set")
async def on_set(variable):
    print(variable.name, variable.value)
```

###`#!python off(key, callback)` { #off data-toc-label="off" }

Removes an event that the connection was listening to.

**PARAMETERS**

- **key** (`#!python str`) - The key of the event to be removed.
- **callback** (`#!python callable`) - The function that runs when the event occurs.

**Example:**

```python
async def on_set(variable):
    print(variable.name, variable.value)

connection.on("set", on_set)
connection.off("set", on_set)

connection.run()
```

###`#!python once(key, callback=None)` { #once data-toc-label="once" }

Adds an event for the connection listen to. The event will only be fired once. This can either be used as a decorator or a function.

**PARAMETERS**

- **key** (`#!python str`) - The key of the event to be listened to.
- **callback** (`#!python callable`) - The function that will run when the event occurs.

**RETURNS** - `#!python None | callable`

**Example:**

```python
# Use as a function
async def on_set(variable):
    print(variable.name, variable.value)

connection.once("set", on_set)

# Use as a decorator
@connection.once("set")
async def on_set(variable):
    print(variable.name, variable.value)
```

###`#!python listeners(event)` { #listeners data-toc-label="listeners" }

Returns all the functions that are attached to the event `#!python event`.

**PARAMETERS**

- **event** (`#!python event`) - The key of the event that you want to retrieve the listeners of.

**RETURNS** - `#!python list[callable]`

**Example:**

```python
@connection.on("set")
async def on_set(variable):
    print(variable.name, variable.value)

print(connection.listeners("set"))
# <function on_set at 0x31290093>

connection.run()
```

## Events

###`handshake`

Fired after the WebSocket connection handshake occurs.

###`connect`

Fired when the WebSocket connection has finished and is ready to receive data.

###`outgoing`

Fired when data is sent to the server.

**PARAMETERS**

- **data** (`#!python str`) - The data that is being sent.

###`change`

Fired when a variable value changes, no matter who changed it.

**PARAMETERS**

- **variable** (`#!python CloudVariable`) - The variable that has been changed, as a [CloudVariable](../CloudVariable).

###`set`

Fired when a variable value changes, by anyone except yourself.

**PARAMETERS**

- **variable** (`#!python CloudVariable`) - The variable that has been changed, as a [CloudVariable](../CloudVariable).

###`create`

Fired when a cloud variable has been created.

**PARAMETERS**

- **variable** (`#!python CloudVariable`) - The variable that has been created, as a [CloudVariable](../CloudVariable).

###`delete`

Fired when a cloud variable has been deleted.

**PARAMETERS**

- **name** (`#!python str`) - The name of the variable that has been deleted. This includes the cloud emoji at the beginning ("☁ ").
