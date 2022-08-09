# **ScrapingSession**

Used to scrape data that isn't provided cleanly by Scratch's website.

## Methods

###`#!python get_follower_count(user)` { #get_follower_count data-toc-label="get_follower_count" }

Gets the follower count of a user.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the follower count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_following_count(user)` { #get_following_count data-toc-label="get_following_count" }

Gets the number of users that a user is following.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the following count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_favorited_count(user)` { #get_favorited_count data-toc-label="get_favorited_count" }

Gets the number of projects that a user has favorited.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the favorite count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_followed_studios_count(user)` { #get_followed_studios_count data-toc-label="get_followed_studios_count" }

Gets the number of studios that a user has followed.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the followed studios count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_curated_studios_count(user)` { #get_curated_studios_count data-toc-label="get_curated_studios_count" }

Gets the number of studios that a user curates.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the curated studios count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_shared_projects_count(user)` { #get_shared_projects_count data-toc-label="get_shared_projects_count" }

Gets the number of projects that a user has shared.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the shared project count of, or a corresponding object representing them.

**RETURNS** - `#!python int`

###`#!python get_user_activity(user, max=100000)` { #get_user_activity data-toc-label="get_user_activity" }

Retrieves a user's activity as an array of [Activity](../Activity) objects.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the activity of, or a corresponding object representing them.
- **max** (`#!python int`) - The maximum amount of items you want to retrieve. Note that there is no harm in making this absurdly large, since user activity from before a year ago is not available.

**RETURNS** - `#!python list[Activity]`

**Example:**

```python
print(session.scraping.get_user_activity("griffpatch", max=1)[0].actor)
# griffpatch
```

###`#!python get_profile_comments(user, all=False, page=1)` { #get_profile_comments data-toc-label="get_profile_comments" }

Gets a list of comments on a user's profile as an array of [ProfileComment](../ProfileComment) objects.

**PARAMETERS**

- **user** (`#!python User | IncompleteUser | str`) - The username of the user you want to retrieve the profile comments of, or a corresponding object representing them.
- **all** (`#!python bool`) - Whether to retrieve all of the user's comments or just one page of them.
- **page** (`#!python page`) - If `#!python all` is `#!python False`, this is the page of profile comments to retrieve.

**RETURNS** - `#!python list[ProfileComment]`

**Example:**

```python
print(session.scraping.get_profile_comments("griffpatch")[0].content)
# Follow me please
```

###`#!python get_signature(post_id, as_html=False)` { #get_signature data-toc-label="get_signature" }

Gets the signature at the bottom of a forum post with the specified ID.

**PARAMETERS**

- **post_id** (`#!python int`) - The ID of the post you want to retrieve the signature from.
- **as_html** (`#!python bool`) - Whether you want the response in HTML or in BBCode. By default, the response is converted to BBCode.

**RETURNS** - `#!python str`

**Example:**

```python
print(session.scraping.get_signature(5154718))
# I use scratch.
# GF: I'll dump you. BF: hex dump or binary dump?
# ...
```
