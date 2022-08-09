# Tests a bunch of stuff, just to make sure it works.
# Mainly just for me to test the library, not meant for
# anyone else.

import time

from scratchclient import ScratchSession

session = ScratchSession()

# Scratch user with semi-average stats
user = session.get_user("codubee")
print(vars(user))
print(user.get_projects(all=True))
print(user.get_curating())
print(user.get_favorites())
print(user.get_following(all=True))
print(user.get_followers())
print(user.get_message_count())
print(user.get_featured_project())

project = session.get_project(104)
print(vars(project))
print(vars(project.get_comment(488)))
print(project.get_scripts())
print(project.get_remixtree())
print(project.get_remixes(all=True))
print(project.get_studios())
print(project.get_comments())

studio = session.get_studio(30136012)
print(vars(studio))
print(studio.get_projects(all=True))
print(studio.get_curators())
print(studio.get_managers(all=True))
print(studio.get_comments())
print(studio.get_activity())

print(session.get_news())
print(session.explore_projects())
print(session.explore_studios(query="test"))
print(session.search_projects(query="the", language="es"))
print(session.search_studios(query="test", mode="trending"))
print(session.get_front_page())
print(session.forums.get_post_source(5154718))
print(vars(session.forums.get_latest_topic_posts(506810)[0]))
print(session.forums.get_latest_category_posts(1))
print(session.scraping.get_signature(6371373))
print(session.scraping.get_signature(6373382))

session = ScratchSession(sys.argv[1], sys.argv[2])

print(session.get_messages())
print(session.get_activity())

print(session.get_own_projects())
print(session.get_own_studios())

project_json = {
    "targets": [
        {
            "isStage": True,
            "name": "Stage",
            "variables": {"`jEk@4|i[#Fk?(8x)AV.-my variable": ["my variable", 0]},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "backdrop1",
                    "dataFormat": "svg",
                    "assetId": "cd21514d0531fdffb22204e0ec5ed84a",
                    "md5ext": "cd21514d0531fdffb22204e0ec5ed84a.svg",
                    "rotationCenterX": 240,
                    "rotationCenterY": 180,
                }
            ],
            "sounds": [
                {
                    "name": "pop",
                    "assetId": "83a9787d4cb6f3b7632b4ddfebf74367",
                    "dataFormat": "wav",
                    "format": "",
                    "rate": 48000,
                    "sampleCount": 1123,
                    "md5ext": "83a9787d4cb6f3b7632b4ddfebf74367.wav",
                }
            ],
            "volume": 100,
            "layerOrder": 0,
            "tempo": 60,
            "videoTransparency": 50,
            "videoState": "on",
            "textToSpeechLanguage": None,
        },
        {
            "isStage": False,
            "name": "Sprite1",
            "variables": {},
            "lists": {},
            "broadcasts": {},
            "blocks": {},
            "comments": {},
            "currentCostume": 0,
            "costumes": [
                {
                    "name": "costume1",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "bcf454acf82e4504149f7ffe07081dbc",
                    "md5ext": "bcf454acf82e4504149f7ffe07081dbc.svg",
                    "rotationCenterX": 48,
                    "rotationCenterY": 50,
                },
                {
                    "name": "costume2",
                    "bitmapResolution": 1,
                    "dataFormat": "svg",
                    "assetId": "0fb9be3e8397c983338cb71dc84d0b25",
                    "md5ext": "0fb9be3e8397c983338cb71dc84d0b25.svg",
                    "rotationCenterX": 46,
                    "rotationCenterY": 53,
                },
            ],
            "sounds": [
                {
                    "name": "Meow",
                    "assetId": "83c36d806dc92327b9e7049a565c6bff",
                    "dataFormat": "wav",
                    "format": "",
                    "rate": 48000,
                    "sampleCount": 40681,
                    "md5ext": "83c36d806dc92327b9e7049a565c6bff.wav",
                }
            ],
            "volume": 100,
            "layerOrder": 1,
            "visible": True,
            "x": 0,
            "y": 0,
            "size": 100,
            "direction": 90,
            "draggable": False,
            "rotationStyle": "all around",
        },
    ],
    "monitors": [],
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0-prerelease.20220601111129",
        "agent": "Mozilla/5.0 (X11; CrOS x86_64 14588.123.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.72 Safari/537.36",
    },
}

project_id = session.create_project(project_json)
project = session.get_project(project_id)
project.love()
project.favorite()
project.unlove()
project.unfavorite()

project_json["meta"][
    "agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
project.save(project_json)
print(project.get_scripts())
project.toggle_commenting()
project.view()
project.set_title("test")
project.share()
project.turn_on_commenting()
comment = project.post_comment("testing")
print(vars(comment))
time.sleep(5)
reply = comment.reply("testing2")
print(vars(reply))
time.sleep(5)
other_comment = project.post_comment("testing3")
other_comment.delete()
project.unshare()
project.delete()

studio = session.get_studio(session.create_studio())
studio.set_title("test")
studio.set_description("test")
studio.add_project(104)
studio.add_project(105)
studio.remove_project(105)
studio.follow()
studio.unfollow()
studio.toggle_commenting()
studio.toggle_commenting()
comment = studio.post_comment("testing")
print(vars(comment))
time.sleep(5)
reply = comment.reply("testing2")
print(vars(reply))
time.sleep(5)
other_comment = studio.post_comment("testing3")
other_comment.delete()
studio.delete()
