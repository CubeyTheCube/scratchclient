# **ProfileComment**

## Properties

###`#!python id : int` { #id data-toc-label="id" }

The ID of the comment.

###`#!python parent_id : int | None` { #parent_id data-toc-label="parent_id" }

If the comment is a reply, this is the ID of its parent comment. Otherwise, it is `#!python None`.

###`#!python commentee_id : int | None` { #commentee_id data-toc-label="commentee_id" }

If the comment is a reply, this is the user ID of the author of the parent comment. Otherwise, it is `#!python None`.

###`#!python content : str` { #content data-toc-label="content" }

The content of the comment.

###`#!python replies : list[ProfileComment]` { #replies data-toc-label="replies" }

A list of the replies to the comment, as an array of [ProfileComment](../ProfileComment) objects.

###`#!python author : str` { #author data-toc-label="author" }

The username of the author of the comment.

###`#!python author_id : int` { #author_id data-toc-label="author_id" }

The user ID of the author of the comment.

###`#!python created_timestamp : str` { #created_timestamp data-toc-label="created_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the comment was created.

###`#!python last_modified_timestamp : str` { #last_modified_timestamp data-toc-label="last_modified_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the comment was last modified.

!!! note
    I have no idea what the hell this means.

###`#!python visible : bool` { #visible data-toc-label="visible" }

A boolean value representing whether the comment has been deleted or not.

###`#!python user : str` { #user data-toc-label="user" }

The username of the user whose profile the comment is on.

## Methods

###`#!python delete()` { #delete data-toc-label="delete" }

Deletes the comment. You must be logged in and the owner of the profile the comment is on for this to not throw an error.

###`#!python report()` { #report data-toc-label="report" }

Reports the comment. You must be logged in for this to not throw an error.

###`#!python reply(content)` { #reply data-toc-label="reply" 
}

Replies to the comment. You must be logged in for this to not throw an error.

**PARAMETERS**

- **content** (`#!python str`) - The content of your reply.

**Example:**

```python
comment = session.scraping.get_profile_comments("griffpatch")[0]
comment.reply("Go away")
```
