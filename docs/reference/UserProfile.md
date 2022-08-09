# **UserProfile**

## Properties

###`#!python user : User` { #user data-toc-label="user" }

A [User](../User) object representing the user whose profile it is.

**Example:**

```python
profile = session.get_user("griffpatch").profile
print(profile.user.id)
# 1882674
```

###`#!python username : str` { #username data-toc-label="username" }

The username of the owner of the profile.

###`#!python id : int` { #id data-toc-label="id" }

The user's profile ID. This is not the same as their user ID.

**Example:**

```python
print(session.get_user("griffpatch").profile.id)
# 1267661
```

###`#!python avatar_URL : str` { #avatar_URL data-toc-label="avatar_URL" }

The URL of the user's avatar (profile picture).

###`#!python bio : str` { #bio data-toc-label="bio" }

The user's bio (the "About Me" section of their profile).

###`#!python status : str` { #status data-toc-label="status" }

The user's status (the "What I'm Working On" section of their profile).

###`#!python country : str` { #country data-toc-label="country" }

The user's country (location).

```python
print(session.get_user("griffpatch").profile.country)
# United Kingdom
```

## Methods

###`#!python set_bio(content)` { #set_bio data-toc-label="set_bio" }

Sets the bio ("About Me" section) of the user's profile to the specified content. You must be logged in and the owner of the profile for this to not throw an error.

**PARAMETERS**

- **content** (`#!python str`) - The content that you want to set the bio to.

**Example:**

```python
profile = session.user.profile

profile.set_bio("I love Scratch :D")
print(profile.bio)
# I love Scratch :D
```

###`#!python set_status(content)` { #set_status data-toc-label="set_status" }

Sets the status ("What I'm Working On" section) of the user's profile to the specified content. You must be logged in and the owner of the profile for this to not throw an error.

**PARAMETERS**

- **content** (`#!python str`) - The content that you want to set the status to.

###`#!python set_avatar(filename)` { #set_avatar data-toc-label="set_avatar" }

Sets the user's avatar (profile picture) to the file with the specified `#!python filename`. You must be logged in and the owner of the profile for this to not throw an error.

**PARAMETERS**

- **filename** (`#!python str`) - The path to a file containing the avatar image. Note that this must be a file, not binary data; if you wish to use binary data, you could try writing the data to a temporary file, then deleting it afterwards.

###`#!python get_featured_project()` { #get_featured_project data-toc-label="get_featured_project" }

Retrieves the featured project of the user. Returns an [IncompleteProject](../IncompleteProject) object representing the project.

**RETURNS** - `#!python IncompleteProject`

**Example:**

```python
print(session.get_user("griffpatch").get_featured_project().id)
# 10128407
```

###`#!python set_featured_project(label, project)` { #set_featured_project data-toc-label="set_featured_project" }

Sets the user's featured project on their profile. You must be logged in and the owner of the profile for this to not throw an error.

**PARAMETERS**

- **label** (`#!python str`) - The label to go above the featured project. Must be one of the following strings:
    - `#!python "featured_project"` - Representing "Featured Project".
    - `#!python "featured_tutorial"` - Representing "Featured Tutorial".
    - `#!python "work_in_progress"` - Representing "Work In Progress".
    - `#!python "remix_this"` - Representing "Remix This".
    - `#!python "my_favorite_things"` - Representing "My Favorite Things".
    - `#!python "why_i_scratch"` - Representing "Why I Scratch".
- **project** (`#!python int | Project | IncompleteProject | RemixtreeProject`) - The project to be set as the featured project. This must either be an `#!python int` representing the project's ID or a corresponding project object.

**Example:**

```python
session.user.profile.set_featured_project("why_i_scratch", 321079301972)
print(session.user.profile.get_featured_project())
# furry art compilation
```
