# **ScratchSession**

## `#!python ScratchSession(username=None, password=None, session_id=None, token=None)` { #ScratchSession data-toc-label="ScratchSession" }
Returns an object representing the user's current session. If a password is not passed, you could pass a session ID and a token to authenticate yourself.

**PARAMETERS**

- **username** (`#!python str | None`) - The username of the user.
  
- **password** (`#!python str | None`) - The password of the user's account - used to log in.
  
- **session_id** (`#!python str | None`) - The session ID of the session - used to authenticate many requests.
  
- **token** (`#!python str | None`) - The token of the user - used to authenticate many requests.

## Properties

###`#!python username : str | None` { #username data-toc-label="username" }

The username of the logged in user.
Will be `#!python None` if the user does not log in.

###`#!python session_id : str | None` { #session_id data-toc-label="session_id" }

The Scratch session ID of the logged in user's session. Required to authenticate most requests to Scratch's old site (scratchr2).
Will be `#!python None` if the user does not log in and no session ID is passed to `#!python ScratchSession`.

###`#!python token : str | None` { #token data-toc-label="token" }

The token of the logged in user. Required to authenticate most requests to Scratch's new site (scratch-www).
Will be `#!python None` if the user does not log in and no token is passed to `#!python ScratchSession`.

###`#!python csrf_token : str | None` { #csrf_token data-toc-label="csrf_token" }

The CSRF token of the logged in user's session. Required for most requests that need authentication.
Will be `#!python None` if the user does not log in or does not provide a session ID or a token.

###`#!python logged_in : bool` { #logged_in data-toc-label="logged_in" }

Whether the user is logged in or not. This is `#!python True` if the user logs in or provides a session ID or a token.

###`#!python user : User` { #user data-toc-label="user" }

The [User](../User) object of the logged in user.
Will be `#!python None` if the user does not log in or does not provide a session ID or a token.

**Example:**

```python
session = ScratchSession("griffpatch", "realpassword")

print(session.user.id)
# 1882674
```

###`#!python forums : ForumSession` { #forums data-toc-label="forums" }

A [ForumSession](../ForumSession) object that allows the user to do things with Scratch's forums.

###`#!python scraping : ScrapingSession` { #scraping data-toc-label="scraping" }

A [ScrapingSession](../ScrapingSession) object that allows the user to scrape data off Scratch pages that are from the old site (scratchr2). These pages do not have JSON APIs, so it is necessary to scrape the HTML of the pages.

```python
session = ScratchSession("griffpatch", "realpassword")

print(session.scraping.get_profile_comments("ceebee")[0].content)
# Pls ban @griffpatch he is hacking my account
```

## Methods

###`#!python get_user(user)` { #get_user data-toc-label="get_user" }

Gets the [User](../User) object of the specified username or user.

**PARAMETERS**

- **user** (`#!python str | IncompleteUser | User`) - The username of the user or an [IncompleteUser](../IncompleteUser) or a [User](../User) object representing it.

**RETURNS** - `#!python User`

**Example:**

```python
print(session.get_user("griffpatch").scratchteam)
# False
```

###`#!python get_project(project)` { #get_project data-toc-label="get_project" }

Gets the [Project](../Project) object for the specified ID or project.

**PARAMETERS**

- **project** (`#!python str | int | IncompleteProject | RemixtreeProject | Project`) - The ID of the project (as either a string or an integer) or an [IncompleteProject](../IncompleteProject), a [RemixtreeProject](../RemixtreeProject), or a [Project](../Project) object representing it.

**RETURNS** - `#!python Project`

**Example:**

```python
print(session.get_project(60917032).title)
# Appel v1.4
```

###`#!python get_studio(id)` { #get_studio data-toc-label="get_studio" }

Gets the [Studio](../Studio) object for the specified ID or studio.

**PARAMETERS**

- **studio** (`#!python str | int | IncompleteStudio | Studio`) - The ID of the studio (as either a string or an integer) or an [IncompleteStudio](../IncompleteStudio) or a [Studio](../Studio) object representing it.

**RETURNS** - `#!python Studio`

**Example:**

```python
print(session.get_studio(26135902).owner)
# Za-Chary
```

###`#!python get_news(all=False, limit=20, offset=0)` { #get_news data-toc-label="get_news" }

Gets Scratch's [news](https://scratch.mit.edu/discuss/5/) as an array of [News](../News) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single news headline or only `#!python limit` headlines.
- **limit** (`#!python Optional[int]`) - How many news headlines to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) - The offset of the headlines from the newest ones - i.e. an offset of 20 would give you the next 20 headlines after the first 20.

**RETURNS** - `#!python list[News]`

**Example:**

```python
print(session.get_news()[0].title)
# Wiki Wednesday!
```

###`#!python get_messages(all=False, limit=20, offset=0, filter="")` { #get_messages data-toc-label="get_messages" }

Gets the messages of the logged in user as an array of [Message](../Message) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve every single message or only `#!python limit` message.
- **limit** (`#!python Optional[int]`) - How many news messages to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) - The offset of the messages from the newest ones - i.e. an offset of 20 would give you the next 20 messages after the first 20.
- **filter** (`#!python Optional[Literal[""] | Literal["comments"] | Literal["projects"] | Literal["studios"] | Literal["forums"]]`) - A filter to apply to the messages. Must be one of the following: an empty string, which does not filter out any messages; `#!python "comments"`, which only includes comment activity; `#!python "projects"`, which only includes project activity; `#!python "studios"`, which only includes studio activity; or `#!python "forums"`, which only includes forum activity.

**RETURNS** - `#!python list[Message]`

**Example:**

```python
print(session.get_messages(all=True)[0].actor)
# griffpatch

print(session.get_messages(limit=40, offset=10, filter="comments")[0].comment_fragment)
# thank you my friend
```

###`#!python create_cloud_connection(project_id, is_async=False, cloud_host="clouddata.scratch.mit.edu", headers={})` { #create_cloud_connection data-toc-label="create_cloud_connection" }

Creates a cloud connection for the specified project ID. Returns a [CloudConnection](../CloudConnection) object if `#!python is_async` is `False`, otherwise it returns an [AsyncCloudConnection](../AsyncCloudConnection) object.

**PARAMETERS**

- **project_id** (`#!python int | string`) - The ID of the project to make a connection to, represented as either a string or an integer.
- **is_async** (`#!python Optional[bool]`) - Whether to return a `#!python CloudConnection` or an `#!python AsyncCloudConnection`. [AsyncCloudConnection](../AsyncCloudConnection) supports asyncio, whereas [CloudConnection](../CloudConnection) is completely synchronous.
- **cloud_host** (`#!python Optional[str]`) - The hostname of the server where the cloud variables are hosted. By default, this is `#!python "clouddata.scratch.mit.edu"`.
- **headers** (`#!python dict`) - Any extra headers to add to the connection's handshake.

**RETURNS** - `#!python CloudConnection | AsyncCloudConnection`

**Example:**

```python
connection = session.create_cloud_connection(104)

print(connection.get_cloud_variable('foo'))
# 1391203129031
```

###`#!python explore_projects(mode="trending", query="*", language="en")` { #explore_projects data-toc-label="explore_projects" }

Explores Scratch projects with the specified `#!python mode` (either `#!python "trending"`, `#!python "popular"`, or `#!python "recent"`), query and language. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **mode** (`#!python Optional[Literal["trending"] | Literal["popular"] | Literal["recent"]]`) - The basis of how the projects are sorted - "trending" projects were popular recently, "popular" projects are popular in general, and "recent" projects are recent in general.
- **query** (`#!python Optional[str]`) - The query used to search for the projects.
- **language** (`#!python Optional[str]`) - The language to search for projects in. Must be an [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) code.

**RETURNS** - `#!python list[Project]`

**Example:**

```python
print(session.explore_projects()[0].title)
# Epic 7D platformer 2021
```

###`#!python explore_studios(mode="trending", query="*")` { #explore_studios data-toc-label="explore_studios" }

Explores Scratch studios with the specified `#!python mode` (either `#!python "trending"`, `#!python "popular"`, or `#!python "recent"`) and query. Returns an array of [Studio](../Studio) objects.

**PARAMETERS**

- **mode** (`#!python  Optional[Literal["trending"] | Literal["popular"] | Literal["recent"]]`) - The basis of how the studios are sorted - "trending" studios were popular recently, "popular" studios are popular in general, and "recent" studios are recent in general.
- **query** (`#!python Optional[str]`) - The query used to search for the studios.

**RETURNS** - `#!python list[Studio]`

###`#!python search_projects(mode="popular", query="*", language="en")` { #search_projects data-toc-label="search_projects" }

Searches Scratch projects with the specified `#!python mode` (either `#!python "trending"` or `#!python "popular"`), `#!python query`, and `#!python language`. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **mode** (`#!python Optional[Literal["trending"] | Literal["popular"]]`) - The basis of how the projects are sorted - "trending" projects were popular recently and "popular" projects are popular in general.
- **query** (`#!python Optional[str]`) - The query used to search for the projects.
- **language** (`#!python Optional[str]`) - The language to search for projects in. Must be an [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) code.

**RETURNS** - `#!python list[Project]`

###`#!python search_studios(mode="popular", query="*")` { #search_studios data-toc-label="search_studios" }

Searches Scratch studios with the specified `#!python mode` and `#!python query`. Returns an array of [Studio](../Studio) objects.

**PARAMETERS**

- **mode** (`#!python Optional[Literal["trending"] | Literal["popular"]])` - The basis of how the studios are sorted - "trending" studios were popular recently and "popular" studios are popular in general.
- **query** (`#!python Optional[str]`) - The query used to search for the studios.

###`#!python get_front_page()` { #get_front_page data-toc-label="get_front_page" }

Gets the data that is used for Scratch's front page. It returns a dictionary containing the following items:

- `#!python "featured_projects"` - Scratch's featured projects; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "featured_studios"` - Scratch's featured studios; an array of [IncompleteStudio](../IncompleteStudio) objects.
- `#!python "top_loved"` - the most loved recent projects; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "top_remixed"` - the most remixed recent projects; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "newest"` - new projects on Scratch; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "scratch_design_studio"` - projects in Scratch's Scratch Design Studio that are on the front page; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "curated"` - projects chosen by the Front Page Curator to be on the front page; an array of [IncompleteProject](../IncompleteProject) objects.
- `#!python "curator"` - the current Front Page Curator; a `#!python str` representing their username.
- `#!python "current_sds"` - the current Scratch Design Studio; an [IncompleteStudio](../IncompleteStudio) object.

**RETURNS** - `#!python dict`

###`#!python get_activity(limit=5, offset=0)` { #get_activity data-toc-label="get_activity" }

Gets your follower's activity (the What's Happening? on the front page). You must be logged in for this to not throw an error. Returns an array of [Activity](../Activity) objects.

**PARAMETERS**

- **limit** (`#!python Optional[int]`) - How many activities to retrieve.
- **offset** (`#!python Optional[int]`) - The offset of the activities from the newest ones - i.e. an offset of 5 would give you the next 5 activites after the first 5.

**RETURNS** - `#!python list[Activity]`

###`#!python create_project(project)` { #create_project data-toc-label="create_project" }

Creates a project. You must be logged in for this to not throw an error. The project will contain the data in the parameter `#!python project`, which should be structured like the `project.json` file in ordinary projects. Returns the ID of the project as an `#!python int`.

**PARAMETERS**

- **project** (`#!python dict`) - The data to be put into the project.

**RETURNS** - `#!python int`

**Example:**

```python
project_json = {"targets":[{"isStage":True,"name":"Stage","variables":{"`jEk@4|i[#Fk?(8x)AV.-my variable":["my variable",0]},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[{"name":"backdrop1","dataFormat":"svg","assetId":"cd21514d0531fdffb22204e0ec5ed84a","md5ext":"cd21514d0531fdffb22204e0ec5ed84a.svg","rotationCenterX":240,"rotationCenterY":180}],"sounds":[{"name":"pop","assetId":"83a9787d4cb6f3b7632b4ddfebf74367","dataFormat":"wav","format":"","rate":48000,"sampleCount":1123,"md5ext":"83a9787d4cb6f3b7632b4ddfebf74367.wav"}],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":None},{"isStage":False,"name":"Sprite1","variables":{},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[{"name":"costume1","bitmapResolution":1,"dataFormat":"svg","assetId":"bcf454acf82e4504149f7ffe07081dbc","md5ext":"bcf454acf82e4504149f7ffe07081dbc.svg","rotationCenterX":48,"rotationCenterY":50},{"name":"costume2","bitmapResolution":1,"dataFormat":"svg","assetId":"0fb9be3e8397c983338cb71dc84d0b25","md5ext":"0fb9be3e8397c983338cb71dc84d0b25.svg","rotationCenterX":46,"rotationCenterY":53}],"sounds":[{"name":"Meow","assetId":"83c36d806dc92327b9e7049a565c6bff","dataFormat":"wav","format":"","rate":48000,"sampleCount":40681,"md5ext":"83c36d806dc92327b9e7049a565c6bff.wav"}],"volume":100,"layerOrder":1,"visible":True,"x":0,"y":0,"size":100,"direction":90,"draggable":False,"rotationStyle":"all around"}],"monitors":[],"extensions":[],"meta":{"semver":"3.0.0","vm":"0.2.0-prerelease.20220601111129","agent":"Mozilla/5.0 (X11; CrOS x86_64 14588.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.72 Safari/537.36"}}

project_id = session.create_project(project)
session.get_project(project_id).share()
```

###`#!python create_studio()` { #create_studio data-toc-label="create_studio" }

Creates a studio. You must be logged in for this to not throw an error. Returns the ID of the studio as an `#!python int`.

**RETURNS** - `#!python int`

###`#!python empty_trash(password)` { #empty_trash data-toc-label="empty_trash" }

Empties your trash (your deleted projects). You must be logged in for this to not throw an error.

**PARAMETERS**

- **password** (`#!python str`) - The password to your account. It's necessary to authenticate this for obvious reasons.

**Example:**

```python
session.get_project(104).delete()
session.empty_trash("hunter2")
```

###`#!python get_own_projects(all=False, sort="", filter="all", page=1)` { #get_own_projects data-toc-label="get_own_projects" }

Gets your own projects, sorted in descending order. You must be logged in for this to not throw an error. Returns an array of [Project](../Project) objects.

**PARAMETERS**

- **all** (`#!python Optiona[boo]l`) - Whether to retrieve a single page of projects or all of them.
- **sort** (`#!python Optional[Literal[""] | Literal["view_count"] | Literal["love_count"] | Literal["remixers_count"] | Literal["title"]]`) - The metric used to sort the projects. Must be one of the following:
    - `#!python ""`
    - `#!python "view_count"`
    - `#!python "love_count"`
    - `#!python "remixers_count"`
    - `#!python "title"`

If it is an empty string, it will be sorted by the date the project was modified.

- **filter** (`#!python Optional[Literal["all"] | Literal["shared"] | Literal["notshared"] | Literal["trashed"]]`) - What the projects are filtered by. Must be one of the following:
    - `#!python "all"`
    - `#!python "shared"`
    - `#!python "notshared"`
    - `#!python "trashed"`
- **page** (`#!python Optional[int]`) - The page of the data - page 1 has the projects that would be top, and they descend from there. Each page has 40 projects.

**RETURNS** - `#!python list[Project]`

**Example:**

```python
print(str.format("My most loved deleted project is {}", session.get_own_projects(sort="love_count", filter="trashed")[0].id))
# My most loved deleted project is 104
```

###`#!python get_own_studios(all=False, sort="", page=1)` { #get_own_studios data-toc-label="get_own_studios" }

Gets your own studios, sorted in descending order. You must be logged in for this to not throw an error. Returns an array of [Studio](../Studio) objects. Note that the `#!python Studio` objects that are returned do not have a `#!python follower_count` or `#!python manager_count` attribute but they do have a `#!python curator_count` attribute.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve a single page of studios or all of them.
- **sort** (`#!python Optional[Literal[""] | Literal["projecters_count"] | Literal["title"]]`) - The metric used to sort the studios. Must be either `#!python ""`, `#!python "projecters_count"`, or `#!python "title"`. If it is an empty string, it will be sorted by the date the studio was modified.
- **page** (`#!python Optional[int]`) - The page of the data - page 1 has the studios that would be top, and they descend from there. Each page has 40 studios.

**RETURNS** - `#!python list[Studio]`

###`#!python upload_asset(asset, file_ext=None)` { #upload_asset data-toc-label="upload_asset" }

Uploads an asset to `assets.scratch.mit.edu`. You must be logged in for this to not throw an error.

**PARAMETERS**

- **asset** (`#!python bytes | str`) - The asset that should be uploaded. If it is an instance of `#!python bytes`, it will be interpreted as binary data, but if it is a `#!python str`, it will be intepreted as a path to a file.
- **file_ext** (`#!python Optional[str | None]`) - The file extension of the asset. It is only necessary when the `#!python asset` parameter is a file name.

###`#!python change_country(country)` { #change_country data-toc-label="change_country" }

Changes the logged in user's country. You must be logged in for this to not throw an error.

**PARAMETERS**

- **country** (`#!python str`) - The country that your country should be changed to.

**Example:**

```python
session.change_country("Antarctica")
```

###`#!python change_password(old_password, new_password)` { #change_password data-toc-label="change_password" }

Changes the logged in user's account's password. You must be logged in for this to not throw an error.

**PARAMETERS**

- **old_password** (`#!python str`) - Your account's current password (for authentication).
- **new_password** (`#!python str`) - The password you want your account's password to be changed to.

###`#!python change_email(new_email, password)` { #change_email data-toc-label="change_email" }

Changes the logged in user's account's email. You must be logged in for this to not throw an error.

**PARAMETERS**

- **new_emaiil** (`#!python str`) - The email you want your account's email to be changed to.
- **password** (`#!python str`) - Your account's password (for authentication).

###`#!python change_email_subscription(activities=False, teacher_tips=False)` { #change_email_subscription data-toc-label="change_email_subscription" }

Sets what you will receive emails from Scratch for. You must be logged in for this to not throw an error.

**PARAMETERS**

- **activities** (`#!python Optional[bool]`) - Whether you'll receive emails for activity ideas for using Scratch at home.
- **teacher_tips** (`#!python Optional[bool]`) - Whether you'll receive emails about product updates for using Scratch in educational settings.

**Example:**

```python
session.change_email_subscription(teacher_tips=True)
# Now I will receive emails about product updates for using Scratch in educational settings
```

###`#!python get_backpack(all=False, limit=20, offset=0)` { #get_backpack data-toc-label="get_backpack" }

Gets the data in your backpack. You must be logged in for thsi to not throw an error. Returns an array of [BackpackItem](../BackpackItem) objects.

**PARAMETERS**

- **all** (`#!python Optional[bool]`) - Whether to retrieve everything in your backpack or just `#!python limit` items.
- **limit** (`#!python Optional[int]`) - How many items to retrieve if `#!python all` is `#!python False`.
- **offset** (`#!python Optional[int]`) - The offset of the items from the newest ones - i.e. an offset of 20 would give you the next 20 items after the first 20.

**RETURNS** - `#!python list[BackpackItem]`

###`#!python add_to_backpack(item_type, body, mime_type, name, thumbnail)` { #add_to_backpack data-toc-label="add_to_backpack" }

Adds an item to your backpack. You must be logged in for this to not throw an error. Returns the item put into the backpack as a [BackpackItem](../BackpackItem) object.

**PARAMETERS**

- **item_type** (`#!python Literal["script"] | Literal["costume"] | Literal["sound"] | Literal["sprite"]`) - The type of item to be put in the backpack. Must be one of the following:
    - `#!python "script"`
    - `#!python "costume"`
    - `#!python "sound"`
    - `#!python "sprite"`
- **body** (`#!python str`) - The base-64-encoded data in the item. If the `#!python item_type` of the item is `#!python "script"` the data must be in the format that it is in the `project.json` file in ordinary projects. If the `#!python item_type` is `#!python "sprite"`, it must be a zipped version of the data in the format that it is in the `project.json` file in ordinary projects. Otherwise, it just has to be the data in the image of the costume or the sound file.
- **mime_type** (`#!python Literal["application/zip"] | Literal["application/json"] | Literal["audio/x-wav"] | Literal["audio/mp3"] | Literal["image/svg+xml"] | Literal["image/png"]`) - The [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) of the data. If the `#!python item_type` is `#!python "script"`, this must be `#!python "application/json"`; if the `#!python item_type` is `#!python "sprite"`, this must be `#!python "application/zip"`; if the `#!python item_type` is `#!python "costume"`, this must be `#!python "image/svg+xml"` or `#!python "image/png"`; and if the `#!python item_type` is `#!python "sound"`, this must be `#!python "audio/mp3"` or `#!python "audio/x-wav"`.
- **name** (`#!python str`) - The name of the item to be added to the backpack. If the `#!python item_type` is `#!python "costume"`, `#!python "sound"`, or `#!python "sprite"`, this is merely the name of the costume, sound, or sprite. If the `#!python item_type` is `#!python "script"`, this must be the string `#!python "code"`.
- **thumbnail** (`#!python str`) - The base-64-encoded thumbnail of the item to be put in the backpack.

**RETURNS** - `#!python BackpackItem`

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
    session.add_to_backpack("costume", body, "image/png", "furry", thumbnail)
```

###`#!python get_statistics()` { #get_statistics data-toc-label="get_statistics" }

Gets site statistics for Scratch. Returns a dictionary with the following items:

- `#!python "overall"` - Overall data for Scratch; a dictionary with the following items:
    - `#!python "COMMENT_COUNT"` - The total number of comments on the site.
    - `#!python "PROFILE_COMMENT_COUNT`" - The total number of profile comments on the site.
    - `#!python "PROJECT_COMMENT_COUNT"` - The total number of project comments on the site.
    - `#!python "STUDIO_COMMENT_COUNT"` - The total number of studio comments on the site.
    - `#!python "USER_COUNT"` - The total number of users on the site.
    - `#!python "PROJECT_COUNT"` - The total number of projects on the site.
    - `#!python "STUDIO_COUNT"` - The total number of studios on the site.
- `#!python "last_month"` - Site data for the past month; a dictionary with the following items:
    - `#!python "pageviews"` - The number of page views for Scratch over the past month.
    - `#!python "visits"` - The number of visits to Scratch's website over the past month.
    - `#!python "users"` - The number of unique visitors to Scratch over the past month.
- `#!python "over_time"` - Site data for Scratch over time, containing the data used to create graphs; a dictionary with the following items:
    <div class="fun-fact-country-parent">
    - `#!python "activity_data"` - Activity trends for Scratch over time. An array of dictionaries with the items `#!python "color"` (a hex code), `#!python "key"` (a `#!python str`), and `#!python "values"` (an array full of dictionaries containing X and Y coordinates).
    - `#!python "active_user_data"` - Data on monthly active users on Scratch. An array of dictionaries with the items `#!python "color"` (a hex code), `#!python "key"` (a `#!python str`), and `#!python "values"` (an array full of dictionaries containing X and Y coordinates).
    - `#!python "age_distribution_data"` - Data on the age distribution of new Scratchers. A dict with the following items:
        - `#!python "key"` - A `#!python str` with the value `#!python "Registration age of Scratchers"`.
        - `#!python "values"` - An array full of dictionaries containing X and Y coordinates used to draw a histogram.
    - `#!python "country_distribution"` - Data on the distribution of the locations of Scratchers. A dictionary with an item for each country, the value being the number of users from the country.

    - !!! fun-fact "Fun Fact"
            There used to be a bug allowing people to change their country to a two-letter code, and the data for those "countries" is still returned here. It also appears that a similar bug was used for 11 people to change their location to "England". Sadly, this bug does not work anymore.

    - `#!python "comment_data"` - Data on distribution of location of comment activity. An array of dictionaries with the items `#!python "color"` (a hex code), `#!python "key"` (a `#!python str`), and `#!python "values"` (an array full of dictionaries containing X and Y coordinates).
    - `#!python "project_data"` - Data on shared projects, representing the distribution of original projects vs. remixed projects. An array of dictionaries with the items `#!python "color"` (a hex code), `#!python "key"` (a `#!python str`), and `#!python "values"` (an array full of dictionaries containing X and Y coordinates).
    </div>

**RETURNS** - `#!python dict`

**Example:**

```python
print(str.format(
    "There have been {} users registered who are from England",
    session.get_statistics()["over_time"]["country_distribution"]["England"],
))
# There have been 11 users registered who are from England
```

###`#!python is_valid_username(username)` { #is_valid_username data-toc-label="is_valid_username" }

Checks if a username can be registered. Returns a `#!python bool` representing whether it can.

**PARAMETERS**

- **username** (`#!python str`) - The username to be checked for availability.

**RETURNS** - `#!python bool`

###`#!python check_password(password)` { #check_password data-toc-label="check_password" }

Checks if the password passed is your account's password. You must be logged in for this to not throw an error. Returns a `#!python bool` representing whether the password is valid.

**PARAMETERS**

- **password** (`#!python str`) - The password to be checked for validity.

**RETURNS** - `#!python bool`

###`#!python logout()`  { #logout data-toc-label="logout" }

Logs out of Scratch. You must be logged in for this to not throw an error.
