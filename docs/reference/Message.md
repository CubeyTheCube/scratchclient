# **Message**

## Properties

###`#!python type : Literal["followuser"] | Literal["loveproject"] | Literal["favoriteproject"] | Literal["addcomment"] | Literal["curatorinvite"] | Literal["remixproject"] | Literal["studioactivity"] | Literal["forumpost"] | Literal["becomeownerstudio"] | Literal["becomehoststudio"] | Literal["userjoin"]` { #type data-toc-label="type" }

The type of message that the message is. This can be any of the following:

- `#!python "followuser"` - Received when someone follows you.
- `#!python "loveproject"` - Received when someone loves one of your projects.
- `#!python "favoriteproject"` - Received when someone favorites one of your projects.
- `#!python "addcomment"` - Received when someone comments on your profile or replies to one of your comments.
- `#!python "curatorinvite"` - Received when you are invited to become a curator of a studio.
- `#!python "remixproject"` - Received when someone remixes one of your projects.
- `#!python "studioactivity"` - Received when there is activity in a studio that you curate.
- `#!python "forumpost"` - Received when there is a post on a forum topic you either follow or own.
- `#!python "becomeownerstudio"` - Received when you become manager of a studio.
!!! note
    I wonder if this is why they changed the name to "host" instead of "owner".
- `#!python "becomehoststudio"` - Received when you become the host of a studio.
- `#!python "userjoin"` - Received when you join Scratch.

###`#!python actor : str` { #actor data-toc-label="actor" }

The username of the person who caused the message to be sent (I.E. the person who sent a comment or caused activity in a studio).

###`#!python actor_id : int` { #actor_id data-toc-label="actor_id" }

The user ID of the person who caused the message to be sent.

###`#!python created_timestamp : str` { #created_timestamp data-toc-label="created_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the message was created.

---

A `#!python Message` might have other attributes depending on its `#!python type`.

###`#!python project_id : int` { #project_id data-toc-label="project_id" }

Appears when the `#!python type` is either `#!python "loveproject"`, `#!python "favoriteproject"` or `#!python "remixproject"`. This is the ID of the project that was loved, favorited, or remixed.

###`#!python title : str` { #title data-toc-label="title" }

Appears when the `#!python type` is either `#!python "loveproject"`, `#!python "remixproject"`, `#!python "curatorinvite"`, or `#!python "studioactivity"`. If the `#!python type` is `#!python "loveproject"` or `#!python "remixproject"`, this is the title of the project where the action occurred. Otherwise, this is the title of the studio where the action occurred.

###`#!python project_title : str` { #project_title data-toc-label="project_title" }

Appears when the `#!python type` is `#!python "favoriteproject"`. This is the title of the project being favorited.

###`#!python parent_id : int` { #parent_id data-toc-label="parent_id" }

Appears when the `#!python type` is `#!python "remixproject"`. This is the ID of the parent project that has been remixed.

###`#!python parent_title : str` { #parent_title data-toc-label="parent_title" }

Appears when the `#!python type` is `#!python "remixproject"`. This is the title of the parent project that has been remixed.

###`#!python comment_id : int` { #comment_id data-toc-label="comment_id" }

Appears when the `#!python type` is `#!python "addcomment"`. This is the ID of the comment that was sent.

###`#!python comment_fragment : str` { #comment_fragment data-toc-label="comment_fragment" }

Appears when the `#!python type` is `#!python "addcomment"`. This is the fragment of the comment that is shown in the message.

###`#!python commentee_username : str | None` { #commentee_username data-toc-label="commentee_username" }

Appears when the `#!python type` is `#!python "addcomment"`. If the comment is a reply, this is the username of the person who was replied to. Otherwise, this is `#!python None`.

###`#!python comment_obj_id : int` { #comment_obj_id data-toc-label="comment_obj_id" }

Appears when the `#!python type` is `#!python "addcomment"`. This is the ID of the user, project, or studio where the comment was posted.

###`#!python comment_obj_title : str` { #comment_obj_title data-toc-label="comment_obj_title" }

Appears when the `#!python type` is `#!python "addcomment"`. If the comment occurred on a studio or project, this is the title of the studio or project. Otherwise, this is the username of the user whose profile the comment was posted on.

###`#!python comment_type : Literal[0] | Literal[1] | Literal[2]` { #comment_type data-toc-label="comment_type" }

Appears when the `#!python type` is `#!python "addcomment"`. If the comment occurred on a project, this is `#!python 0`. If it occurred on a profile, this is `#!python 1`. If it occurred on a studio, this is `#!python 2`.

###`#!python gallery_id : int` { #gallery_id data-toc-label="gallery_id" }

Appears when the `#!python type` is `#!python "curatorinvite"`, `#!python "studioactivity"`, `#!python "becomeownerstudio"`, or `#!python "becomehoststudio"`. This is the ID of the studio where the action occurred.

###`#!python gallery_title : str` { #gallery_title data-toc-label="gallery_title" }

Appears when the `#!python type` is `#!python "becomeownerstudio"`, or `#!python "becomehoststudio"`. This is the title of the studio where the action occurred.

###`#!python topic_id : int` { #topic_id data-toc-label="topic_id" }

Appears when the `#!python type` is `#!python "forumpost"`. This is the ID of the topic where the post occurred.

###`#!python topic_title : str` { #topic_title data-toc-label="topic_title" }

Appears when the `#!python type` is `#!python "forumpost"`. This is the title of the topic where the post occurred.
