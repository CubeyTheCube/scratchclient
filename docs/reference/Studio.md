# **Studio**

## Properties

###`#!python id : int` { #id data-toc-label="id" }

The ID of the studio.

**Example:**

```python
print(session.get_studio(14).id)
# 14
```

###`#!python title : str` { #title data-toc-label="title" }

The title of the studio.

**Example:**

```python
print(session.get_studio(14).title)
# Citizen Schools @ ML-14
```

###`#!python host : int` { #host data-toc-label="host" }

The user ID of the host (owner) of the studio.

###`#!python description : str` { #description data-toc-label="description" }

The description of the studio.

###`#!python visible : bool` { #visible data-toc-label="visible" }

A boolean value representing whether the studio is deleted or not.

###`#!python open_to_public : bool` { #open_to_public data-toc-label="open_to_public" }

A boolean value representing whether anyone can add projects to the studio.

###`#!python comments_allowed : bool` { #comments_allowed data-toc-label="comments_allowed" }

A boolean value representing if comments are allowed on the studio.

###`#!python thumbnail_URL : str` { #thumbnail_URL data-toc-label="thumbnail_URL" }

The URL of the thumbnail of the studio.

###`#!python created_timestamp : str` { #created_timestamp data-toc-label="created_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the studio was created.

**Example:**

```python
import datetime

def iso_to_readable(iso):
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    date = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    date.astimezone(timezone)

    return date.strftime("%Y-%m-%d %I:%M %p")

print(iso_to_readable(session.get_studio(14).created_timestamp))
# 2008-05-03 1:01 PM
```

###`#!python last_modified_timestamp : str` { #last_modified_timestamp data-toc-label="last_modified_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the description or thumbnail of the studio was most recently modified.

###`#!python curator_count : int | None` { #curator_count data-toc-label="curator_count" }

The number of curators the studio has.

###`#!python follower_count : int | None` { #follower_count data-toc-label="follower_count" }

The number of followers the studio has.

###`#!python manager_count : int | None` { #manager_count data-toc-label="manager_count" }

The number of managers the studio has.

###`#!python curator_count : int | None` { #curator_count data-toc-label="curator_count" }

The number of curators the studio has.

###`#!python project_count : int | None` { #project_count data-toc-label="project_count" }

The number of projects the studio has.

## Methods

###`#!python get_comment(comment_id)` { #get_comment data-toc-label="get_comment" }

Gets a comment on the studio with the ID `#!python comment_id` as a [StudioComment](../StudioComment) object.

**PARAMETERS**

- **comment_id** (`#!python int`) - The comment ID of the comment to be retrieved

**RETURNS** - `#!python StudioComment`

**Example:**

```python
print(session.get_studio(14).get_comment(25224).content)
# I was born there
```

###`#!python add_project(project)` { #add_project data-toc-label="add_project" }

Adds a project to the studio. You must be logged in and have permission to add projects to the studio for this to not throw an error.

**PARAMETERS**

- **project** (`#!python int | str | IncompleteProject | RemixtreeProject | Project`) - The project to be added to the studio, either as an `#!python int` or `#!python str` representing the project's ID, or a corresponding project object.

###`#!python remove_project(project)` { #remove_project data-toc-label="remove_project" }

Removes a project from the studio. You must be logged in and be a curator of the studio for this to not throw an error.

**PARAMETERS**

- **project** (`#!python int | str | IncompleteProject | RemixtreeProject | Project`) - The project to be removed from the studio, either as an `#!python int` or `#!python str` representing the project's ID, or a corresponding project object.

###`#!python get_projects(all=False, limit=20, offset=0)` { #get_projects data-toc-label="get_projects" }

Gets a list of projects in the studio. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single project or just `#!python limit` projects.
- **limit** (`#!python Optional[int]`) - How many projects to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the projects from the newest ones - i.e. an offset of 20 would give you the next 20 projects after the first 20.

**RETURNS** - `#!python list[Project]`

**Example:**

```python
print(session.get_studio(14).get_projects()[0].title)
# football, basket and baseball
```

###`#!python get_curators(all=False, limit=20, offset=0)` { #get_curators data-toc-label="get_curators" }

Gets a list of the curators of the studio. Returns an array of [User](../User) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single curator or just `#!python limit` curators.
- **limit** (`#!python Optional[int]`) - How many curators to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the curators from the newest ones - i.e. an offset of 20 would give you the next 20 curators after the first 20.

**RETURNS** - `#!python list[User]`

**Example:**

```python
print(session.get_studio(30136012).get_curators()[0].username)
# wvj
```

###`#!python get_managers(all=False, limit=20, offset=0)` { #get_managers data-toc-label="get_managers" }

Gets a list of the managers of the studio. Returns an array of [User](../User) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single manager or just `#!python limit` managers.
- **limit** (`#!python Optional[int]`) - How many managers to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the managers from the newest ones - i.e. an offset of 20 would give you the next 20 managers after the first 20.

**RETURNS** - `#!python list[User]`

**Example:**

```python
print(session.get_studio(30136012).get_managers()[0].username)
# CatsUnited
```

###`#!python get_roles()` { #get_roles data-toc-label="get_roles" }

Retrieves the roles the logged-in user has in the studio. You must be logged in for this to not throw an error. Returns a `#!python dict` containing the following items:

- **manager** (`#!python bool`) - Whether you are a manager of the studio.
- **curator** (`#!python bool`) - Whether you are a curator of the studio.
- **invited** (`#!python bool`) - Whether you have a pending invitation to the studio.
- **following** (`#!python bool`) - Whether you are following the studio.

**RETURNS** - `#!python dict`

**Example:**

```python
studio = session.get_studio(14)
print(studio.get_roles()["following"])
# False
studio.follow()
print(studio.get_roles()["following"])
# True
```

###`#!python follow()` { #follow data-toc-label="follow" }

Follows the studio. You must be logged in for this to not throw an error.

###`#!python unfollow()` { #unfollow data-toc-label="unfollow" }

Unfollows the studio. You must be logged in for this to not throw an error.

###`#!python open_to_public()` { #open_to_public data-toc-label="open_to_public" }

Opens the studio to the public so anyone can add projects. You must be logged in and a manager of the studio for this to not throw an error.

###`#!python close_to_public()` { #close_to_public data-toc-label="close_to_public" }

Closes the studio to the public so only curators can add projects. You must be logged in and a manager of the studio for this to not throw an error.

###`#!python toggle_commenting()` { #toggle_commenting data-toc-label="toggle_commenting" }

Toggles the ability for people to comment in the studio. You must be logged in and a manager of the studio for this to not throw an error.

**Example:**

```python
studio = session.get_studio(30136012)
studio.post_comment("Scratch sucks so I'm closing this studio")
studio.toggle_commenting()
```

###`#!python get_comments(all=False, limit=20, offset=0)` { #get_comments data-toc-label="get_comments" }

Gets a list of comments on the studio. Returns an array of [StudioComment](../StudioComment) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single comment or just `#!python limit` comments.
- **limit** (`#!python Optional[int]`) - How many comments to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the comments from the newest ones - i.e. an offset of 20 would give you the next 20 comments after the first 20.

**RETURNS** - `#!python list[StudioComment]`

**Example:**

```python
print(session.get_studio(30136012).get_comments()[0].content)
# hot take: we should ban all people that don't like scratch
```

###`#!python get_activity(all=False, limit=20, offset=0)` { #get_activity data-toc-label="get_activity" }

Gets the activity in the studio. Returns an array of [Activity](../Activity) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single activity or just `#!python limit` activities.
- **limit** (`#!python Optional[int]`) - How many activities to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the activities from the newest ones - i.e. an offset of 20 would give you the next 20 activities after the first 20.

**RETURNS** - `#!python list[Activity]`

**Example:**

```python
print(session.get_studio(30136012).get_activity()[0].type)
# addprojectostudio
```

###`#!python post_comment(content, parent_id="", commentee_id="")` { #post_comment data-toc-label="post_comment" }

Posts a comment on the studio. You must be logged in for this to not throw an error. Returns the posted comment as a `#!python StudioComment`.

**PARAMETERS**

- **content** (`#!python str`) - The content of the comment to be posted.
- **parent_id** (`#!python Optional[Literal[""] | int]`) - If the comment to be posted is a reply, this is the comment ID of the parent comment. Otherwise, this is an empty string `#!python ""`.
- **commentee_id** (`#!python Optiona[Literal[""] | int]`) - If the comment to be posted is a reply, this is the user ID of the author of the parent comment. Otherwise, this an empty string `#!python ""`.

**RETURNS** - `#!python StudioComment`

**Example:**

```python
session.get_project(14).post_comment("OMG first studio on Scratch")
session.get_project(14).post_comment("OMG first comment on the first studio on scratch", parent_id=25224, commentee_id=35153)
```

###`#!python delete_comment(comment_id)` { #delete_comment data-toc-label="delete_comment" }

Deletes a comment on the studio. You must be logged in, a manager of the studio, and the author of the comment, for this to not throw an error.

!!! warning

    This is deprecated. It's recommended to use `#!python StudioComment.delete` instead. See [this](../StudioComment#delete) for more details.

**PARAMETERS**

- **comment_id** (`#!python int`) - The ID of the comment to be deleted.

###`#!python report_comment(comment_id)` { #report_comment data-toc-label="report_comment" }

Reports a comment on the studio. You must be logged in for this to not throw an error.

!!! warning

    This is deprecated. It's recommended to use `#!python StudioComment.report` instead. See [this](../StudioComment#report) for more details.

**PARAMETERS**

- **comment_id** (`#!python int`) - The ID of the comment to be reported.

###`#!python invite_curator(user)` { #invite_curator data-toc-label="invite_curator" }

Invites a user to become a curator of the studio. You must be logged in, and a manager of the studio, for this to not throw an error.

**PARAMETERS**

- **user** (`#!python str | User | IncompleteUser`) - The username of the user to be invited, or an object representing the user.

###`#!python accept_curator(user)` { #accept_curator data-toc-label="accept_curator" }

Accepts any pending curator invitations to the studio. You must be logged in, and having been invited to be a curator of the studio, for this to not throw an error.

###`#!python promote_curator(user)` { #promote_curator data-toc-label="promote_curator" }

Promotes a user to a manager of the studio. You must be logged in, and a manager of the studio, for this to not throw an error.

**PARAMETERS**

- **user** (`#!python str | User | IncompleteUser`) - The username of the user to be promoted, or an object representing the user. The user must already be a curator for this to not throw an error.

###`#!python transfer_host(user, password)` { #transfer_host data-toc-label="transfer_host" }

Transfers ownership of the studio. You must be logged in, and the host of the studio, for this to not throw an error.

**PARAMETERS**

- **user** (`#!python str | User | IncompleteUser`) - The username of the user that will become the new host, or an object representing the user. The user must already be a manager for this to not throw an error.
- **password** (`#!python str`) - The password to your account. This is necessary for authentication.

###`#!python set_description(description)` { #set_description data-toc-label="set_description" }

Sets the description of the studio. You must be logged in, and the host of the studio, for this to not throw an error.

**PARAMETERS**

**description** (`#!python str`) - The description that the description of the studio should be set to.

###`#!python set_title(content)` { #set_title data-toc-label="set_title" }

Sets the title of the studio. You must be logged in, and the host of the studio, for this to not throw an error.

**PARAMETERS**

**content** (`#!python str`) - The title that the title of the studio should be set to.

###`#!python set_thumbnail(file_or_data)` { #set_thumbnail data-toc-label="set_thumbnail" }

Sets the thumbnail of the studio. You must be logged in, and the host of the studio, for this to not throw an error.

**PARAMETERS**

**file_or_data** (`#!python bytes | str`) - The file that the thumbnail should be set to. If this is a `#!python str`, then it will be interpreted as a path to a file; otherwise, it will be interpreted as the data in the image.

###`#!python delete()` { #delete data-toc-label="delete" }

Deletes the studio. You must be logged in, and the host of the studio, for this to not throw an error.