# Simultaneous Connections

This shows how to use scratchclient's asynchronous features to have two simulataneous cloud connections to different projects.

```python title="message_passer.py"
# Passes messages between two projects, a pretty simple concept
# Both projects have variables called "Request" and "Received"

import asyncio
from scratchclient import ScratchSession

session = ScratchSession("griffpatch", "hunter2")

# These would be replaced with your actual project IDs
connections = [
    session.create_cloud_connection(1239123091, is_async=True), 
    session.create_cloud_connection(1285894890, is_async=True)
]

for i, connection in enumerate(connections):
    @connection.on("set")
    async def on_set(variable):
        if variable.name == "Request":
            other_connection = connections[1 - i]
            await other_connection.set_cloud_variable("Received", variable.value)

coroutines = [connection.connect() for connection in connections]
asyncio.run(asyncio.gather(*coroutines))
```
