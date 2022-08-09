# **RemixtreeProject**

A class that represents the project data that is used on Scratch's remix tree page.

## Properties

###`#!python title : str` { #title data-toc-label="title" }

The title of the project.

###`#!python id : int` { #id data-toc-label="id" }

The project ID of the project.

###`#!python author : str` { #author data-toc-label="author" }

The username of the project's creator.

An `#!python IncompleteProject` might have other attributes depending on where it came from:

###`#!python moderation_status : str` { #moderation_status data-toc-label="moderation_status" }

The moderation status of the project. This is either `#!python "notreviewed"` or `#!python "notsafe"`. If it is `#!python "notsafe"` (NSFE), this means the project can't show up in search results, the front page, or the trending page.

**Example:**

```python
def is_nsfe(project_id):
  remixtree = session.get_project(project_id).get_remixtree()
  try:
    remixtree_project = next(project for project in remixtree if project.id == project_id)
  except StopIteration:
    # It's unknown since the project has no remix tree
    return False

  return remixtree_project.moderation_status == "notsafe"

print(is_nsfe(414601586))
# True
```

!!! fun-fact

    Although you can easily determine whether a project is NSFE using this, you are not allowed to mention how to do this or say that a project is NSFE on Scratch. It's weird that they still include this in an API response, though. Just think of it as a little Easter Egg in Scratch's API.

###`#!python visible : bool` { #visible data-toc-label="visible" }

A boolean value representing whether the project has been deleted or not.

###`#!python is_published : bool` { #is_published data-toc-label="is_published" }

A boolean value representing whether the project has been shared or not.

###`#!python love_count : int` { #love_count data-toc-label="love_count" }

The number of loves the project has.

###`#!python favorite_count : int` { #favorite_count data-toc-label="favorite_count" }

The number of favorites the project has.

###`#!python created_timestamp : int` { #created_timestamp data-toc-label="created_timestamp" }

A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) representing the date the project was created.

**Example:**

```python
import datetime

def unix_to_readable(unix):
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    date = datetime.datetime.fromtimestamp(unix)
    date.astimezone(timezone)

    return date.strftime("%Y-%m-%d %I:%M %p")

project_104 = next(project for project in 
session.get_project(104).get_remix_tree() if project.id == 104)
print(unix_to_readable(project_104.created_timestamp))
# 2007-03-05 10:47 AM
```

###`#!python last_modified_timestamp : int` { #last_modified_timestamp data-toc-label="last_modified_timestamp" }

A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) timestamp representing the date the project was most recently modified.

###`#!python shared_timestamp : int | None` { #shared_timestamp data-toc-label="shared_timestamp" }

A [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) timestamp representing the date the project was shared.

###`#!python parent_id : int | None` { #parent_id data-toc-label="parent_id" }

If the project is a remix, this is the ID of the project's parent project. Otherwise, it's `#!python None`.

###`#!python children : list[int]` { #children data-toc-label="children" }

A list of the project IDs of the project's remixes.

!!! note

    This can be used to determine the project's remixes much more quickly than [`Project.get_remixes`](../Project#get_remixes).
    