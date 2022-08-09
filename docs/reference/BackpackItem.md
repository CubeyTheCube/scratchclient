# **BackpackItem**

## Properties

###`#!python id : str` { #id data-toc-label="id" }

The ID of the backpack item (a UUID).

###`#!python name : str` { #name data-toc-label="name" }

The name of the item.

###`#!python body_URL : str` { #body_URL data-toc-label="body_URL" }

The URL of the content of the item.

###`#!python thumbnail_URL : str` { #thumbnail_URL data-toc-label="thumbnail_URL" }

The URL of the thumbnail of the item.

###`#!python mime : Literal["application/zip"] | Literal["application/json"] | Literal["audio/x-wav"] | Literal["audio/mp3"] | Literal["image/svg+xml"] | Literal["image/png"]` { #mime data-toc-label="mime" }

The MIME type of the item.

###`#!python type : Literal["script"] | Literal["costume"] | Literal["sound"] | Literal["sprite"]` { #type data-toc-label="type" }

The type of item that the item is.

## Methods

###`#!python delete()` { #delete data-toc-label="delete" }

Deletes the item.

**Example:**

```python
import base64
from PIL import Image
from io import BytesIO

costume_file = open("furry.png", "rb")
body = base64.b64encode(costume_file.read())

image = Image.open("furry.png")
with BytesIO() as f:
    image.save(f, format="JPEG")
    thumbnail = base64.b64encode(f.getvalue())
    item = session.add_to_backpack("costume", body, "image/png", "furry", thumbnail)
    item.delete()
```
