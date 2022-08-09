# **Activity**

## Properties

###`#!python type : Literal["followuser"] | Literal["followstudio"] | Literal["loveproject"], Literal["favoriteproject"] | Literal["remixproject"] | Literal["becomecurator"] | Literal["becomeownerstudio"] | Literal["shareproject"] | Literal["addprojecttostudio"] | Literal["removeprojectstudio"] | Literal["updatestudio"] | Literal["removecuratorstudio"] | Literal["becomehoststudio"]` { #type data-toc-label="type" }

The type of activity that the activity is. This can be any of the following:

- `#!python "followuser"` - Occurs when the actor follows someone.
- `#!python "followstudio"` - Occurs when the actor follows a studio.
- `#!python "loveproject"` - Occurs when the actor loves a project.
- `#!python "favoriteproject"` - Occurs when the actor favorites a project.
- `#!python "remixproject"` - Occurs when the actor remixes a project.
- `#!python "becomecurator"` - Occurs when someone becomes a curator of a studio.
- `#!python "becomeownerstudio"` - Occurs when someone is promoted to manager of a studio.
- `#!python "becomehoststudio"` - Occurs when someone becomes the host of a studio.
- `#!python "shareproject"` - Occurs when the actor shares a project.
- `#!python "addprojectotstudio"` - Occurs when someone adds a project to a studio.
- `#!python "removeprojectstudio"` - Occurs when someone removes a project from a studio.
- `#!python "updatestudio"` - Occurs when someone updates the title, thumbnail, or description of a studio.
- `#!python "removecuratorstudio"` - Occurs when a curator is removed from a studio.

###`#!python actor : str` { #actor data-toc-label="actor" }

The username of the person who caused the actvity (I.E. the person who loved a project or updated the title of a studio).

###`#!python created_timestamp : str` { #created_timestamp data-toc-label="created_timestamp" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the activity was created.

---

A `#!python Activity` might have other attributes depending on its `#!python type` and where it came from.

###`#!python actor_id : int` { #actor_id data-toc-label="actor_id" }

Appears everywhere except from calls to [ScrapingSession.get_user_activity](../ScrapingSession#get_user_activity). This is the user ID of the actor who caused the activity.

###`#!python id : str` { #id data-toc-label="id" }

The ID of the activity. Appears only from calls to [Studio.get_activity](../Studio#get_activity). This is the activity `#!python type` followed by a hyphen `-` and some numbers.

###`#!python followed_username : str` { #followed_username data-toc-label="followed_username" }

Appears when the `#!python type` is `#!python "followuser"`. This is the username of the user who has been followed.

###`#!python project_id : int` { #project_id data-toc-label="project_id" }

Appears when the `#!python type` is either `#!python "loveproject"`, `#!python "favoriteproject"` or `#!python "remixproject"`. This is the ID of the project that was loved, favorited, or remixed.

###`#!python title : str` { #title data-toc-label="title" }

Appears when the `#!python type` is either `#!python "followstudio"`, `#!python "loveproject"`, `#!python "remixproject"`, `#!python "becomecurator"`, or `#!python "shareproject"`. If the activity was related to a studio, this is the title of the studio it involved. Otherwise, this is the title of the project it involved.

###`#!python project_title : str` { #project_title data-toc-label="project_title" }

Appears when the `#!python type` is `#!python "favoriteproject"`, `#!python "addprojecttostudio"`, or `#!python "removeprojectfromstudio"`. This is the title of the project that the activity involves.

###`#!python parent_id : int` { #parent_id data-toc-label="parent_id" }

Appears when the `#!python type` is `#!python "remixproject"`. This is the ID of the parent project that has been remixed.

###`#!python parent_title : str` { #parent_title data-toc-label="parent_title" }

Appears when the `#!python type` is `#!python "remixproject"`. This is the title of the parent project that has been remixed.

###`#!python recipient_username : str` { #recipient_username data-toc-label="recipient_username" }

Appears when the `#!python type` is `#!python "becomeownerstudio"` or `#!python "becomehoststudio"`. This is the username of the user who has become manager or host of the studio.

###`#!python username : str` { #username data-toc-label="username" }

Appears when the `#!python type` is `#!python "becomecurator"` or `#!python "removecuratorstudio"`. This is the username of the person who added or removed the curator.

###`#!python gallery_id : int` { #gallery_id data-toc-label="gallery_id" }

Appears when the `#!python type` is `#!python "followstudio"`, `#!python "becomecurator"`, or `#!python "becomeownerstudio"`. This is the ID of the studio where the action occurred.

###`#!python gallery_title : str` { #gallery_title data-toc-label="gallery_title" }

Appears when the `#!python type` is `#!python "becomeownerstudio"`. This is the title of the studio where the action occurred.
