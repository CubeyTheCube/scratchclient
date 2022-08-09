# **ForumSession**

## Methods

###`#!python create_topic(category_id, title, body)` { #create_topic data-toc-label="create_topic" }

Creates a forum topic. You must be logged in for this to not throw an error.

**PARAMETERS**

- **category_id** (`#!python int | str`) - The ID of the forum category you want to post in. For example, the ID of the "Suggestions" category is `#!python 31`.
- **title** (`#!python str`) - The title of the original post in the topic.
- **body** (`#!python str`) - The body of the original post in the topic.

**Example:**

```python
session.forums.create_topic(1, "Add like button to comments", "Title.\nSupporters:\n\nNobody yet!")
```

###`#!python post(topic_id, content)` { #post data-toc-label="post" }

Posts a forum post on the specified topic.

**PARAMETERS**

- **topic_id** (`#!python int | str`) - The ID of the topic you want to post on.
- **content** (`#!python str`) - The content of the post.

**Example:**

```python
session.forums.post(506810, "This sucks")
```

###`#!python edit_post(post_id, content)` { #edit_post data-toc-label="edit_post" }

Edits the forum post with the specified ID.

**PARAMETERS**

- **post_id** (`#!python int | str`) - The ID of the post you want to edit.
- **content** (`#!python str`) - The new content of the post.

###`#!python report_post(post_id, reason)` { #report_post data-toc-label="report_post" }

Reports the forum post with the specified ID.

**PARAMETERS**

- **post_id** (`#!python int | str`) - The ID of the post you want to report.
- **reason** (`#!python str`) - The reason you want to report the post.

###`#!python get_post_source(post_id)` { #get_post_source data-toc-label="get_post_source" }

Gets the BBCode source of the forum post with the specified ID.

**PARAMETERS**

- **post_id** (`#!python int | str`) - The ID of the post.

**RETURNS** - `#!python str`

###`#!python follow_topic(topic_id)` { #follow_topic data-toc-label="follow_topic" }

Follows the forum topic with the specified ID.

**PARAMETERS**

- **topic** (`#!python int | str`) - The ID of the topic you want to follow.

###`#!python unfollow_topic(topic_id)` { #unfollow_topic data-toc-label="unfollow_topic" }

Unfollows the forum topic with the specified ID.

**PARAMETERS**

- **topic** (`#!python int | str`) - The ID of the topic you want to unfollow.

###`#!python change_signature(signature)` { #change_signature data-toc-label="change_signature" }

Changes your forum signature to a new signature.

**PARAMETERS**

- **signature** (`#!python str`) - The signature you want to change your signature to.

###`#!python get_latest_topic_posts(topic_id)` { #get_latest_topic_posts data-toc-label="get_latest_topic_posts" }

Gets the latest posts on the specified forum topic. Returns an array of [ForumPost](../ForumPost) objects.

**PARAMETERS**

- **topic_id** (`#!python int | str`) - The ID of the topic you want to get the latest posts on.

**RETURNS** - `#!python list[ForumPost]`

**Example:**

```python
print(session.forums.get_latest_topic_posts(506810)[0].content)
# scratchclient sucks
```

###`#!python get_latest_category_posts(category_id)` { #get_latest_category_posts data-toc-label="get_latest_category_posts" }

Gets the latest posts on the specified forum category. Returns an array of [ForumPost](../ForumPost) objects.

**PARAMETERS**

- **topic_id** (`#!python int | str`) - The ID of the category you want to get the latest posts on. For example, the ID of the "Suggestions" forum category is `#!python 1`.

**RETURNS** - `#!python list[ForumPost]`

**Example:**

```python
print(session.forums.get_latest_category_posts(31)[0].content)
# scratchclient sucks
```
