# Stats Viewer

This is the server code for a "stats viewer" project.

```python title="stats_viewer.py"
# This stats viewer can retrieve a user's follower and following count
# This assumes that the project has four cloud variables: "Follower Count Request",
# "Follower Count Response", "Following Count Request",
# and "Following Count Response". The "Follower Count Request" and
# "Following Count Request" variables will be set
# by people using the project, and will contain the username of the user
# requesting the data, a delimiter, and the username of the user for which 
# they want the statistics. The "Follower Count Response" and "Following Count Response"
# variables will be set by the server (this program) and will contain the username
# of the user who sent the request, a delimiter, and the number of followers.


from scratchclient import ScratchSession

session = ScratchSession("griffpatch", "badpassword")

character_set = " abcdefghijklmnopqrstuvwxyz1234567890-_"

def decode_request(request):
    # An example request would be something like 02150200101505
    # If you decode this using the character set, it would become "Bob", then a space, then "Joe"
    # Bob is the user who sent the request and Joe is the user that which they want to know the follower count of
    decoded = ""
    for i in range(0, len(request), 2):
        # This loops through the request, two characters at a time
        decoded += character_set[int(request[i: i+2])]

    # Split it into the requester and the requested username
    return request.split(" ")

def encode_response(username, count):
    # An example response would be something like 021502001000
    # Everything until the first instead of 00 will be decoded
    # and the decoded value is "Bob". After that is the actual
    # follower count
    response = ""
    for char in username:
        # Add a 0 to the beginning of the number if there isn't any
        response += str(character_set.index(char)).zfill(2)

    response += f"00{count}"
    return response
    

# You would replace the number with your actual project ID
connection = session.create_cloud_connection(1032938129)

# This means that the `on_set` function will run every time someone else changes a cloud variable.
@connection.on("set")
def on_set(variable):
    if variable.name == "Follower Count Request" or variable.name == "Following Count Request":
        requester_username, requested_username = decode_request(variable.value)
        count = session.scraping.get_follower_count(requested_username)
        if variable.name == "Follower Count Request"
        else session.scraping.get_following_count(requested_username)

        # We need to encode the requester username so the client
        # knows which response is theirs and not someone else's
        response = encode_response(requester_username, count)

        # The response variable name is the same name with "Request"
        # replaced with "Response"
        response_variable_name = variable.name.replace("Request", "Response")
        connection.set_cloud_variable(response_variable_name, response)
```
