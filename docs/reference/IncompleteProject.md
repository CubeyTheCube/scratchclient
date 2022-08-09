# **IncompleteProject**

A class that represents a project with less data than a [Project](../Project) object.

## Properties

###`#!python title : str` { #title data-toc-label="title" }

The title of the project.

###`#!python id : int` { #id data-toc-label="id" }

The project ID of the project.

###`#!python author : str` { #author data-toc-label="author" }

The username of the project's creator.

###`#!python thumbnail_URL : str` { #thumbnail_URL data-toc-label="thumbnail_URL" }

The URL of the project's thumbnail.

---

An `#!python IncompleteProject` might have other attributes depending on where it came from:

###`#!python type : Literal["project"]` { #type data-toc-label="type" }

This is a string that is always `#!python "project"`. It only appears when returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python love_count : int` { #love_count data-toc-label="love_count" }

The number of loves the project has. It only appears when returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python remixers_count : int` { #remixers_count data-toc-label="remixers_count" }

The number of remixes the project has. It only appears in the `#!python "top_remixed"` and `#!python scratch_design_studio` items of the dictionary returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python curator_name : str` { #curator_name data-toc-label="curator_name" }

The username of Scratch's current Front Page Curator. It only appears in the `#!python "curated"` item when returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python gallery_id : int` { #gallery_id data-toc-label="gallery_id" }

The ID of Scratch's current Scratch Design Studio. It only appears in the `#!python "scratch_design_studio"` item when returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python gallery_title : str` { #gallery_title data-toc-label="gallery_title" }

The title of Scratch's current Scratch Design Studio. It only appears in the `#!python "scratch_design_studio"` item when returned from a call to [`ScratchSession.get_front_page`](../ScratchSession#get_front_page).

###`#!python creator_id : int` { #creator_id data-toc-label="creator_id" }

The user ID of the project's creator. It only appears when returned from a call to [`Studio.get_projects`](../Studio#get_projects).

###`#!python avatar : dict` { #avatar data-toc-label="avatar" }

A dictionary containing different images with the author's avatar (profile picture). Contains the items `#!python "90x90"`, `#!python "60x60"`, `#!python "55x55"`, `#!python "50x50"`, and `#!python "32x32"`, either corresponding to a URL to a different size of the avatar. It only appears when returned from a call to [`Studio.get_projects`](../Studio#get_projects).

###`#!python actor_id : int` { #actor_id data-toc-label="actor_id" }

The user ID of the user who added the project to the studio. It only appears when returned from a call to [`Studio.get_projects`](../Studio#get_projects).

###`#!python datetime_modified : str` { #datetime_modified data-toc-label="datetime_modified" }

An [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) timestamp representing the date the project was last modified. It only appears when returned from a call to [`UserProfile.get_featured_project`](../UserProfile#get_featured_project).
