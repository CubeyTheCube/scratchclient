# **User**

## Properties

###`#!python username : str` { #username data-toc-label="username" }

The username of the user.

**Example:**

```python
print(session.get_user("you").username)
# you
```

###`#!python id : int` { #id data-toc-label="id" }

The ID of the user.

###`#!python joined_timestamp : str` { #joined_timestamp data-toc-label="joined_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the user joined Scratch.

###`#!python scratchteam : bool` { #scratchteam data-toc-label="scratchteam" }

A `#!python bool` representing whether the user is a member of the Scratch Team.

###`#!python profile : UserProfile` { #profile data-toc-label="profile" }

A [UserProfile](../UserProfile) object representing data related to the user's profile.

**Example:**

```python
print(session.get_user("mres").profile.bio)
# I'm a professor at MIT Media Lab. But more important: I'm one of the people who created Scratch!
```

## Methods

###`#!python get_projects(all=False, limit=20, offset=0)` { #get_projects data-toc-label="get_projects" }

Gets a list of the user's shared projects. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single project or just `#!python limit` projects.
- **limit** (`#!python Optional[int]`) - How many projects to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the projects from the newest ones - i.e. an offset of 20 would give you the next 20 projects after the first 20.

**RETURNS** - `#!python list[Project]`

**Example:**

```python
print(session.get_user("griffpatch").get_projects(all=True)[-1].title)
# Pacman HD with full Ghost AI (Scratch 2)
```

###`#!python get_curating(all=False, limit=20, offset=0)` { #get_curating data-toc-label="get_curating" }

Gets a list of studios the user is curating. Returns an array of [Studio](../Studio) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single studio or just `#!python limit` studios.
- **limit** (`#!python Optional[int]`) - How many studios to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the studios from the newest ones - i.e. an offset of 20 would give you the next 20 studios after the first 20.

**RETURNS** - `#!python list[Studio]`

**Example:**

```python
print(session.get_user("griffpatch").get_studios()[0].title)
# The Scratchnapped Series (The epic adventures of Scratch?)
```

###`#!python get_favorites(all=False, limit=20, offset=0)` { #get_favorites data-toc-label="get_favorites" }

Gets a list of projects the user has favorited. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single project or just `#!python limit` projects.
- **limit** (`#!python Optional[int]`) - How many projects to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the projects from the newest ones - i.e. an offset of 20 would give you the next 20 projects after the first 20.

**RETURNS** - `#!python list[Project]`

###`#!python get_followers(all=False, limit=20, offset=0)` { #get_followers data-toc-label="get_followers" }

Gets a list of users that are following the user. Returns an array of [User](../User) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single follower or just `#!python limit` followers.
- **limit** (`#!python Optional[int]`) - How many followers to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the followers from the newest ones - i.e. an offset of 20 would give you the next 20 followers after the first 20.

**RETURNS** - `#!python list[User]`

**Example:**

```python
print(session.get_user("griffpatch").get_followers()[0].username)
# kaj
```

###`#!python get_following(all=False, limit=20, offset=0)` { #get_following data-toc-label="get_following" }

Gets a list of users that the user is following. Returns an array of [User](../User) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single user or just `#!python limit` users.
- **limit** (`#!python Optional[int]`) - How many users to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) -  The offset of the users from the newest ones - i.e. an offset of 20 would give you the next 20 users after the first 20.

**RETURNS** - `#!python list[User]`

**Example:**

```python
print(session.get_user("World_Languages").get_following()[0].username)
# RykerJohnson
```

###`#!python get_message_count()` { #get_message_count data-toc-label="get_message_count" }

Gets the message count of the user. Returns an `#!python int` with the user's message count.

!!! info

    Scratch has historically tried to block requests that are trying to retrieve message counts. To prevent weird errors or further restrictions, try to use this sparingly.

**RETURNS** - `#!python int`

**Example:**

```python
print(session.get_user("isthistaken123").get_message_count())
# 90722
```

###`#!python post_comment(content, parent_id="", commentee_id="")` { #post_comment data-toc-label="post_comment" }

Posts a comment on the user's profile. You must be logged in for this to not throw an error.

**PARAMETERS**

- **content** (`#!python str`) - The content of the comment to be posted.
- **parent_id** (`#!python Optional[Literal[""] | int]`) - If the comment to be posted is a reply, this is the comment ID of the parent comment. Otherwise, this is an empty string `#!python ""`.
- **commentee_id** (`#!python Optiona[Literal[""] | int]`) - If the comment to be posted is a reply, this is the user ID of the author of the parent comment. Otherwise, this an empty string `#!python ""`.

**Example:**

```python
session.get_user("isthistaken123").post_comment("hello my friend", parent_id=140441449, commentee_id=143585)
session.get_user("griffpatch").post_comment("f4f?!?!?!")
```

###`#!python delete_comment(comment_id)` { #delete_comment data-toc-label="delete_comment" }

Deletes a comment on the user's profile with the specified `#!python comment_id`. You must be logged in, and be the owner of the profile, for this to not throw an error.

**PARAMETERS**

- **comment_id** (`#!python int`) - The ID of the comment to be deleted.

###`#!python report_comment(comment_id)` { #report_comment data-toc-label="report_comment" }

Reports a comment on the user's profile with the specified `#!python comment_id`. You must be logged in for this to not throw an error.

**PARAMETERS**

- **comment_id** (`#!python int`) - The ID of the comment to be reported.

###`#!python report(field)` { #report data-toc-label="report" }

Reports the user for the reason specified in the `#!python field` parameter. You must be logged in for this to not throw an error.

**PARAMETERS**

- **field** (`#!python Literal["username"] | Literal["icon"] | Literal["description"] | Literal["working_on"]`) - The section of the user's profile that you are reporting them for. A value of `#!python "username"` represents the user's username, a value of `#!python "icon"` represents the user's avatar, a value of `#!python "description"` represents the "About Me" section of the user's profile, and a value of `#!python "working_on"` represents the "What I'm Working On" section of the user's profile.

**Example**
```python
session.get_user("griffpatch_alt").report("username")
```

###`#!python toggle_commenting()` { #toggle_comments data-toc-label="toggle_comments" }

Toggles whether people can post comments on the user's profile. You must be logged in, and the owner of the profile, for this to not throw an error.

**Example:**

```python
session.user.post_comment("Aight im leaving scratch, unless I can get 4000 followers by tonight im out")
session.user.toggle_commenting()
```

###`#!python follow()` { #follow data-toc-label="follow" }

Follows the user. You must be logged in for this to not throw an error. Returns a `#!python dict` with general data about the user's profile.

**RETURNS** - `#!python dict`

**Example**
```python
session.get_user('griffpatch').follow()
```

###`#!python unfollow()` { #unfollow data-toc-label="unfollow" }

Unfollows the user. You must be logged in for this to not throw an error. Returns a `#!python dict` with general data about the user's profile.

**RETURNS** - `#!python dict`

**Example**
```python
griffpatch = session.get_user('griffpatch')

griffpatch.unfollow()
griffpatch.post_comment("I thought we promised we'd do f4f :(")
```
