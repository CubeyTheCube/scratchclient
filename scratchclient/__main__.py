import sys
import datetime
import shutil
from html.parser import HTMLParser
from xml.etree import ElementTree

from .ScratchSession import ScratchSession

NEWLINE = "\n"


class HTMLToTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.text += "\n"

    def handle_data(self, data):
        self.text += data


def html_to_text(html):
    parser = HTMLToTextParser()
    parser.feed(html)

    return parser.text


def iso_to_readable(iso):
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    date = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    date.astimezone(timezone)

    return date.strftime("%Y-%m-%d %I:%M %p")


def separator():
    return "-" * shutil.get_terminal_size((80, 20))[0]


def bold(text):
    return "\033[1m{0}\033[0m".format(text)


session = ScratchSession()


def help():
    print(
        """Usage: scratchclient [COMMAND] [arguments...]
scratchclient allows you to access data from the Scratch website (https://scratch.mit.edu)

Examples:
  scratchclient user griffpatch # Get griffpatch's user data
  scratchclient project 104 # Get data on Scratch project 104
  scratchclient studio 123 # Get data on Scratch studio 123
  scratchclient news # Get latest news on the Scratch website
  scratchclient topic 506810 # Get the latest posts on forum topic 506810
  scratchclient forum 1 # Get the latest posts in the "Suggestions" forum category
    """
    )


def user_data(username):
    try:
        user = session.get_user(username)
    except KeyError:
        print(f"User '{username}' not found")
        return

    print(
        f"""Username: {user.username}
User ID: {user.id}
Joined: {iso_to_readable(user.joined_timestamp)}
Status: {"Scratch Team" if user.scratchteam else "Scratcher or New Scratcher"}
Avatar: {user.profile.avatar_URL}
Country: {user.profile.country}
Profile ID: {user.profile.id}

{separator()}

About me: {user.profile.bio}

What I'm working on: {user.profile.status}

{separator()}

Follower count: {session.scraping.get_follower_count(user)}
Following count: {session.scraping.get_following_count(user)}
Shared projects count: {session.scraping.get_shared_projects_count(user)}
    """
    )


def project_data(project_id):
    try:
        project = session.get_project(project_id)
    except KeyError:
        print(f"Project {project_id} not found")
        return

    print(
        f"""Title: {project.title}
Project ID: {project.id}
Shared: {project.is_published}
Comments on: {"Yes" if project.comments_allowed else "No"}
Thumbnail: {project.thumbnail_URL}
Created: {iso_to_readable(project.created_timestamp)}
Last modified: {iso_to_readable(project.last_modified_timestamp)}
Shared: {iso_to_readable(project.shared_timestamp)}

{separator()}

View count: {project.view_count}
Love count: {project.love_count}
Favorite count: {project.favorite_count}
Remix count: {project.remix_count}

{separator()}

{f'''
Remix of: {project.parent}
Original project: {project.root}

{separator()}

''' if project.is_remix else ""}
Author username: {project.author.username}
Author ID: {project.author.id}
Author status: {"Scratch Team" if project.author.scratchteam else "Scratcher or New Scratcher"}
Author join time: {iso_to_readable(project.author.joined_timestamp)}
Author avatar: {project.author.avatar_URL}

{separator()}

{f"Instructions: {project.instructions}{NEWLINE}" if project.instructions else ""}
{f"Notes and Credits: {project.description}" if project.description else ""}
    """
    )


def studio_data(studio_id):
    try:
        studio = session.get_studio(studio_id)
    except KeyError:
        print(f"Studio {studio_id} not found")
        return

    print(
        f"""Title: {studio.title}
Studio ID: {studio.id}
Host ID: {studio.host}
Comments on: {"Yes" if studio.comments_allowed else "No"}
Thumbnail: {studio.thumbnail_URL}
Open to everyone: {studio.open_to_public}
Created: {iso_to_readable(studio.created_timestamp)}
Last modified: {iso_to_readable(studio.last_modified_timestamp)}

{separator()}

Comment count: {studio.comment_count}
Project count: {studio.project_count}
Manager count: {studio.manager_count}
Follower count: {studio.follower_count}

{separator()}

Description: {studio.description}
    """
    )


def news_data():
    all_news = session.get_news()
    for news in all_news:
        print(bold(news.title))
        print(news.description)
        print(iso_to_readable(news.timestamp))
        print(news.src)

        if news is not all_news[-1]:
            print("\n{0}\n".format(separator()))


def topic_data(topic_id):
    try:
        posts = session.forums.get_latest_topic_posts(topic_id)
    except ElementTree.ParseError:
        print(f"Topic {topic_id} not found")
        return

    for post in posts:
        print(
            f"""{bold(post.title)}
{post.link} | {iso_to_readable(post.published)}

By {post.author}
{separator()}
{html_to_text(post.content)}
        """
        )
        if post is not posts[-1]:
            print("\n{0}\n".format(separator()))


def forum_category_data(category_id):
    try:
        posts = session.forums.get_latest_category_posts(category_id)
    except ElementTree.ParseError:
        print(f"Category {category_id} not found")
        return

    for post in posts:
        print(
            f"""{bold(post.title)}
{post.link} | {iso_to_readable(post.published)}

By {post.author}
{separator()}
{html_to_text(post.content)}
        """
        )
        if post is not posts[-1]:
            print("\n{0}\n".format(separator()))


if len(sys.argv) == 1:
    help()
    exit()
    
command = sys.argv[1]
if command == "help":
    help()
elif command == "user":
    user_data(sys.argv[2])
elif command == "project":
    project_data(sys.argv[2])
elif command == "studio":
    studio_data(sys.argv[2])
elif command == "news":
    news_data()
elif command == "topic":
    topic_data(sys.argv[2])
elif command == "forum":
    forum_category_data(sys.argv[2])
else:
    print(
        """Usage: scratchclient [COMMAND] [arguments...]
Try 'scratchclient help' for more information.
    """
    )
