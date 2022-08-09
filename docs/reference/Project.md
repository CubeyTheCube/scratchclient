# **Project**

## Properties

###`#!python id : int` { #id data-toc-label="id" }

The ID of the project.

**Example:**

```python
print(session.get_project(104).id)
# 104
```

###`#!python title : str` { #title data-toc-label="title" }

The title of the project.

**Example:**

```python
print(session.get_project(104).title)
# Weekend
```

###`#!python instructions : str` { #instructions data-toc-label="instructions" }

The instructions of the project.

###`#!python description : str` { #description data-toc-label="description" }

The description of the project (the "Notes and Credits" field).

###`#!python visible : bool` { #visible data-toc-label="visible" }

A boolean value representing whether the project is deleted or not.

###`#!python public : bool` { #public data-toc-label="public" }

A boolean value representing whether the project is shared or not.

###`#!python comments_allowed : bool` { #comments_allowed data-toc-label="comments_allowed" }

A boolean value representing if comments are allowed on the project.

###`#!python is_published : bool` { #is_published data-toc-label="is_published" }

A boolean value representing whether the project has been shared or not.

!!! note
    I'm not all too sure about the difference between `#!python public` and `#!python is_published`, but I believe the difference is that projects that have `#!python is_published` as `#!python True` could be unshared, but taken down by the Scratch Team, whereas `#!python public` projects must be visible to everyone.

###`#!python author : IncompleteUser` { #author data-toc-label="author" }

The author of the project as an [IncompleteUser](../IncompleteUser) object.

###`#!python thumbnail_URL : str` { #thumbnail_URL data-toc-label="thumbnail_URL" }

The URL of the thumbnail of the project.

###`#!python created_timestamp : str` { #created_timestamp data-toc-label="created_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the project was created.

**Example:**

```python
import datetime

def iso_to_readable(iso):
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    date = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    date.astimezone(timezone)

    return date.strftime("%Y-%m-%d %I:%M %p")

print(iso_to_readable(session.get_project(104).created_timestamp))
# 2007-03-05 10:47 AM
```

###`#!python last_modified_timestamp : str` { #last_modified_timestamp data-toc-label="last_modified_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the project was most recently modified.

###`#!python shared_timestamp : str` { #shared_timestamp data-toc-label="shared_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the project was shared.

###`#!python view_count : int` { #view_count data-toc-label="view_count" }

The number of views the project has.

###`#!python love_count : int` { #love_count data-toc-label="love_count" }

The number of loves (hearts) the project has.

###`#!python favorite_count : int` { #favorite_count data-toc-label="favorite_count" }

The number of favorites (stars) the project has.

###`#!python remix_count : int` { #remix_count data-toc-label="remix_count" }

The number of remixes the project has.

###`#!python parent : int | None` { #parent data-toc-label="parent" }

If the project is a remix, this is the project ID of the immediate parent of the project (the project it was remixed from). Otherwise, this is `#!python None`.

###`#!python root : int | None` { #root data-toc-label="root" }

If the project is a remix, this is the project ID of the root project of the project (the original project it was remixed from). Otherwise, this is `#!python None`.

**Example:**

```python
project = session.get_project(149159110)

print(f"""
Based on project {project.parent}.
Thanks to the original project {project.root}.
""")
```

###`#!python is_remix : bool | None` { #is_remix data-toc-label="is_remix" }

A boolean value representing whether the project is a remix.

## Methods

###`#!python get_comment(comment_id)` { #get_comment data-toc-label="get_comment" }

Gets a comment on the project with the ID `#!python comment_id` as a [ProjectComment](../ProjectComment) object.

**PARAMETERS**

- **comment_id** (`#!python int`) - The comment ID of the comment to be retrieved

**RETURNS** - `#!python ProjectComment`

**Example:**

```python
print(session.get_project(104).get_comment(488).content)
# I personally like it fuzz
```

###`#!python love()` { #love data-toc-label="love" }

Loves the project. Returns a `#!python bool` representing whether the user has loved the project.

**RETURNS** - `#!python bool`


###`#!python unlove()` { #unlove data-toc-label="unlove" }

Unloves the project. Returns a `#!python bool` representing whether the user has loved the project.

**RETURNS** - `#!python bool`


###`#!python favorite()` { #favorite data-toc-label="favorite" }

Favorites the project. Returns a `#!python bool` representing whether the user has favorited the project.

**RETURNS** - `#!python bool`


###`#!python unfavorite()` { #unfavorite data-toc-label="unfavorite" }

Unfavorites the project. Returns a `#!python bool` representing whether the user has favorited the project.

**RETURNS** - `#!python bool`

###`#!python get_scripts()` { #get_scripts data-toc-label="get_scripts" }

Gets the scripts in the project, as a `#!python dict` with the same structure as the `project.json` file found in projects.

**RETURNS** - `#!python dict`

**Example:**

```python
scripts = session.get_project(104).get_scripts()

print(f"The first sprite is called '{scripts['targets'][1]['name']}'")
# The first sprite is called 'girl'
```

###`#!python save(project)` { #save data-toc-label="save" }

Saves the project with the scripts specified in the parameter `#!python project`.

**PARAMETERS**

- **project** (`#!python dict`) - The scripts to be put in the project, with the same format as the `project.json` file found in ordinary projects.

###`#!python get_remixes(all=False, limit=20, offset=0)` { #get_remixes data-toc-label="get_remixes" }

Gets a list of remixes of the project. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single remix or just `#!python limit` remixes.
- **limit** (`#!python Optional[int]`) - How many remixes to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the remixes from the newest ones - i.e. an offset of 20 would give you the next 20 remixes after the first 20.

**RETURNS** - `#!python list[Project]`

**Example:**

```python
print(session.get_project(10128407).get_remixes()[0].title)
# Paper Minecraft 3D
```

###`#!python get_studios(all=False, limit=20, offset=0)` { #get_studios data-toc-label="get_studios" }

Gets a list of studios the project is in. Returns an array of [Studio](../Studio) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single studio or just `#!python limit` studios.
- **limit** (`#!python Optional[int]`) - How many studios to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the studios from the newest ones - i.e. an offset of 20 would give you the next 20 studios after the first 20.

**RETURNS** - `#!python list[Studio]`

**Example:**

```python
print(session.get_project(10128407).get_studios()[0].title)
# Griffpatch's epic games!!
```

###`#!python get_remixtree()` { #get_remixtree data-toc-label="get_remixtree" }

Gets the data in the tree of remixes of the project. This data is used to construct the `remixtree` page ([this](https://scratch.mit.edu/projects/104/remixtree/) is an example) Returns an array of [RemixtreeProject](../RemixtreeProject) objects, which is a list of the projects in the tree.

**RETURNS** - `#!python list[RemixtreeProject]`

**Example:**

```python
print(session.get_project(104).get_remixtree()[0].title)
# Weekend Remake
```

###`#!python get_comments(all=False, limit=20, offset=0)` { #get_comments data-toc-label="get_comments" }

Gets a list of comments on the project. Returns an array of [ProjectComment](../ProjectComment) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single comment or just `#!python limit` comments.
- **limit** (`#!python Optional[int]`) - How many comments to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the comments from the newest ones - i.e. an offset of 20 would give you the next 20 comments after the first 20.

**RETURNS** - `#!python list[ProjectComment]`

**Example:**

```python
print(session.get_project(10128407).get_comments()[0].content)
# follow me please
```

###`#!python get_cloud_logs(all=False, limit=20, offset=0)` { #get_cloud_logs data-toc-label="get_cloud_logs" }

Gets the cloud logs on the project. Returns an array of `#!python dict`s containing the logs.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single log or just `#!python limit` logs.
- **limit** (`#!python Optional[int]`) - How many logs to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the logs from the newest ones - i.e. an offset of 20 would give you the next 20 logs after the first 20.

**RETURNS** - `#!python list[dict]`

**Example:**

```python
print(session.get_project(12785898).get_cloud_logs()[0]["verb"])
# set_var
```

###`#!python post_comment(content, parent_id="", commentee_id="")` { #post_comment data-toc-label="post_comment" }

Posts a comment on the project. You must be logged in for this to not throw an error. Returns the posted comment as a `#!python ProjectComment`.

**PARAMETERS**

- **content** (`#!python str`) - The content of the comment to be posted.
- **parent_id** (`#!python Optional[Literal[""] | int]`) - If the comment to be posted is a reply, this is the comment ID of the parent comment. Otherwise, this is an empty string `#!python ""`.
- **commentee_id** (`#!python Optiona[Literal[""] | int]`) - If the comment to be posted is a reply, this is the user ID of the author of the parent comment. Otherwise, this an empty string `#!python ""`.

**RETURNS** - `#!python ProjectComment`

**Example:**

```python
session.get_project(104).post_comment("OMG first project on Scratch")
session.get_project(104).post_comment("OMG first comment on the first project on scratch", parent_id=488, commentee_id=6493)
```

###`#!python get_visibility()` { #get_visibility data-toc-label="get_visibility" }

Gets the visibility and moderation status of the project. You must be logged in and the owner of the project for this to not throw an error. Returns the data as a `#!python dict`, with the following items:

- **projectId** - The ID of the project (an `#!python int`).
- **creatorId** - The user ID of the creator of the project (an `#!python int`).
- **deleted** - Whether or not the project is deleted (a `#!python bool`).
- **censored** - Whether the project was censored -- this could either be automatically or by the Scratch Team (a `#!python bool`).
- **censoredByAdmin** - Whether the project was censored by the Scratch Team (a `#!python bool`).
- **censoredByCommunity** - Whether the project was censored automatically by community reports (a `#!python bool`).
- **reshareable** - Whether the project can be reshared (a `#!python bool`).
- **message** - If the project was censored, this is the message from the Scratch Team containing the reason why the project was censored. Otherwise, this is an empty string `#!python ""`.

**RETURNS** - `#!python dict`

**Example:**

```python
print(session.get_project(391293821809312).get_visibility()["censoredByAdmin"])
# True
```

###`#!python toggle_commenting()` { #toggle_comments data-toc-label="toggle_comments" }

Toggles whether people can post comments on the project. You must be logged in, and the owner of the project, for this to not throw an error. Returns the project.

**RETURNS** - `#!python Project`

###`#!python turn_on_commenting()` { #turn_on_commenting data-toc-label="turn_on_commenting" }

Enables commenting on the project. You must be logged in, and the owner of the project, for this to not throw an error. Returns the project.

**RETURNS** - `#!python Project`

###`#!python turn_off_commenting()` { #turn_off_commenting data-toc-label="turn_off_commenting" }

Disables commenting on the project. You must be logged in, and the owner of the project, for this to not throw an error. Returns the project.

**RETURNS** - `#!python Project`

**Example:**

```python
project = session.get_project(19032190120)
project.post_comment("Closing comments until this project gets 100 loves")
project.turn_off_commenting()
```

###`#!python report(category, reason, image=None)` { #report data-toc-label="report" }

Reports the project, for the specified `#!python category` and `#!python reason`. You must be logged in for this to not throw an error.

**PARAMETERS**

- **category** (`#!python str`) - The category of reasons that the rules were broken with the project. Possible valid values are the following:
    - `#!python "0"` - The project is an exact copy of another project.
    - `#!python "1"` - The project uses images or music without credit.
    - `#!python "3"` - The project contains inappropriate language.
    - `#!python "4"` - The project contains inappropriate music.
    - `#!python "5"` - The project shares personal contact information.
    - `#!python "8"` - The project contains inappropriate images.
    - `#!python "9"` - The project is misleading or tricks the community.
    - `#!python "10"` - The project contains a face reveal.
    - `#!python "11"` - The project disallows remixing.
    - `#!python "12"` - You are concerned about the creator's safety.
    - `#!python "13"` - Some other reason.
    - `#!python "14"` - The project contains scary images.
    - `#!python "15"` - The project has a jumpscare.
    - `#!python "16"` - The project contains a violent event.
    - `#!python "17"` - The project contains realistic weapons.
    - `#!python "18"` - The project threatens or bullies another Scratcher.
    - `#!python "19"` - The project is disrespectful to a Scratcher or group.
- **reason** (`#!python str`) - Additional info regarding the location of the offending content within the project.
- **image** (`#!python Optional[str | None]`) - The base-64-encoded thumbnail of the project.

**Example:**

```python
session.get_project(104).report("10", "the guy's face is in the project")
```

###`#!python unshare()` { #unshare data-toc-label="unshare" }

Unshares the project. You must be logged in, and the owner of the project, for this to not throw an error.

###`#!python share()` { #share data-toc-label="share" }

Shares the project. You must be logged in, and the owner of the project, for this to not throw an error.

###`#!python delete()` { #delete data-toc-label="delete" }

Deletes the project. You must be logged in, and the owner of the project, for this to not throw an error.

###`#!python restore_deleted()` { #restore_deleted data-toc-label="restore_deleted" }

Restores the project if it has been deleted. You must be logged in, and the owner of the project, for this to not throw an error.

###`#!python view()` { #view data-toc-label="view" }

Views the project (increments its view count).

!!! warning

    This is incredibly easy to abuse, but do not as the Scratch Team will not be happy, and they will be able to figure out who you are. Furthermore, this is heavily ratelimited, so it's not very effective anyway.

###`#!python set_thumbnail(file_or_data)` { #set_thumbnail data-toc-label="set_thumbnail" }

Sets the thumbnail of the project. You must be logged in, and the owner of the project, for this to not throw an error.

**PARAMETERS**

**file_or_data** (`#!python bytes | str`) - The file that the thumbnail should be set to. If this is a `#!python str`, then it will be interpreted as a path to a file; otherwise, it will be interpreted as the data in the image.

###`#!python set_title(title)` { #set_title data-toc-label="title" }

Sets the title of the project. You must be logged in, and the owner of the project, for this to not throw an error.

**PARAMETERS**

**title** (`#!python str`) - The title that the title of the project should be set to.

**Example:**

```python
session.get_project(130921903123).set_title("4D platformer #games #all ?mode=trending")
```

###`#!python set_instructions(instructions)` { #set_instructions data-toc-label="set_instructions" }

Sets the instructions of the project. You must be logged in, and the owner of the project, for this to not throw an error.

**PARAMETERS**

**instructions** (`#!python str`) - The instructions that the instructions of the project should be set to.

###`#!python set_description(description)` { #set_description data-toc-label="set_description" }

Sets the description (the "Notes and Credits" field) of the project.

**PARAMETERS**

**description** (`#!python str`) - The description that the description of the project should be set to. You must be logged in, and the owner of the project, for this to not throw an error.
