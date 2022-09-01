import requests
import re
from datetime import datetime
import html
from html.parser import HTMLParser

from .User import User
from .Comment import ProfileComment
from .Activity import Activity


def get_attr(attrs_list, attr):
    try:
        val = next(value for key, value in attrs_list if key == attr)
    except StopIteration:
        return None
    else:
        return val


class ActivityParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.current_activity = None
        self.current_attrib = None
        self.message = None
        self.last_attrib = None
        self.id = None
        self.first_title = None
        self.second_id = None
        self.activities = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.current_activity = {}
        elif tag == "a":
            if not self.message:
                return

            self.current_attrib = "link"

            if self.id:
                self.second_id = re.search("\d+", get_attr(attrs, "href")).group()
                return

            possible_id = re.search("\d+", get_attr(attrs, "href"))
            self.id = possible_id.group() if possible_id else None
        elif get_attr(attrs, "class"):
            self.current_attrib = get_attr(attrs, "class")
            self.last_attrib = self.current_attrib

    def handle_data(self, data):
        if self.current_attrib == "actor":
            self.current_activity["actor_username"] = data
        elif self.current_attrib == "link":
            title = data
            message = self.message

            if message.startswith("shared the project"):
                activity_type = "shareproject"

                self.current_activity["project_title"] = title
                self.current_activity["project_id"] = self.id
            elif message.startswith("remixed"):
                if not self.second_id:
                    self.first_title = title
                    return

                activity_type = "remixproject"
                self.current_activity["parent_title"] = self.first_title
                self.current_activity["parent_id"] = self.id
                self.current_activity["project_title"] = title
                self.current_activity["project_id"] = self.second_id
            elif message.startswith("loved"):
                activity_type = "loveproject"

                self.current_activity["project_title"] = title
                self.current_activity["project_id"] = self.id
            elif message.startswith("favorited"):
                activity_type = "favoriteproject"

                self.current_activity["project_title"] = title
                self.current_activity["project_id"] = self.id
            elif message.startswith("is now following the studio"):
                activity_type = "followstudio"

                self.current_activity["gallery_title"] = title
                self.current_activity["gallery_id"] = self.id
            elif message.startswith("is now following"):
                activity_type = "followuser"

                self.current_activity["followed_username"] = title
            elif message.startswith("became a curator of"):
                activity_type = "becomecurator"

                self.current_activity["gallery_title"] = title
                self.current_activity["gallery_id"] = self.id
            elif message.startswith("was promoted to manager of"):
                activity_type = "becomeownerstudio"

                self.current_activity["gallery_title"] = title
                self.current_activity["gallery_id"] = self.id
            elif message.startswith("added"):
                if not self.second_id:
                    self.first_title = title
                    return

                activity_type = "addprojecttostudio"
                self.current_activity["project_title"] = self.first_title
                self.current_activity["project_id"] = self.id
                self.current_activity["gallery_title"] = title
                self.current_activity["gallery_id"] = self.second_id

            self.current_activity["type"] = activity_type
        elif self.current_attrib == "time":
            self.current_activity["datetime_created"] = self.parse_relative_date(data)
        elif self.last_attrib == "actor":
            self.message = data.strip()

    def handle_endtag(self, tag):
        if tag == "li":
            self.activities.append(Activity(self.current_activity))

        self.message = None
        self.last_attrib = self.current_attrib
        self.current_attrib = None
        self.id = None
        self.first_title = None
        self.second_id = None

    def parse_relative_date(self, date):
        UNITS = {
            "second": 1,
            "seconds": 1,
            "minute": 60,
            "minutes": 60,
            "hour": 60 * 60,
            "hours": 60 * 60,
            "day": 24 * 60 * 60,
            "days": 24 * 60 * 60,
            "week": 7 * 24 * 60 * 60,
            "weeks": 7 * 24 * 60 * 60,
            "month": 30 * 24 * 60 * 60,
            "months": 30 * 24 * 60 * 60,
        }

        if date.startswith("in"):
            sign = 1
            date = date[3:]
        else:
            sign = -1
            date = date[:-4]

        relative = sign * sum(
            int(amount) * UNITS[unit]
            for amount, unit in (part.split("\xa0") for part in date.split(", "))
        )

        now = datetime.now().timestamp()

        return datetime.fromtimestamp(now + relative).isoformat()


class ProfileCommentsParser(HTMLParser):
    def __init__(self, user, client):
        super().__init__()

        self.current_comments = []
        self.current_attr = None
        self.comments = []

        self._user = user
        self._client = client

    def handle_starttag(self, tag, attrs):
        if self.current_attr == "content":
            self.current_comments[0]["content"] += str.format(
                "<{0} {1}>", tag, " ".join(f'{key}="{value}"' for key, value in attrs)
            )

            return

        current_class = get_attr(attrs, "class")

        if tag == "li":
            is_top_level = len(self.current_comments) == 0
            self.current_comments.insert(
                0,
                {
                    "visibility": "visible",
                    "author": {},
                    "parent_id": None
                    if is_top_level
                    else self.current_comments[-1]["id"],
                    "commentee_id": None
                    if is_top_level
                    else self.current_comments[-1]["author"]["id"],
                    "replies": [],
                },
            )
        elif tag == "div":
            if current_class == "comment ":
                self.current_comments[0]["id"] = int(get_attr(attrs, "data-comment-id"))
            elif current_class == "name":
                self.current_attr = "name"
            elif current_class == "content":
                self.current_attr = "content"
                self.current_comments[0]["content"] = ""
        elif tag == "span" and current_class == "time":
            self.current_comments[0]["datetime_created"] = get_attr(attrs, "title")
            self.current_comments[0]["datetime_modified"] = get_attr(attrs, "title")
        elif tag == "a":
            if get_attr(attrs, "id") == "comment-user":
                self.current_comments[0]["author"]["username"] = get_attr(
                    attrs, "data-comment-user"
                )
            elif current_class == "reply":
                self.current_comments[0]["author"]["id"] = int(
                    get_attr(attrs, "data-commentee-id")
                )
        elif tag == "img" and current_class == "avatar":
            src = get_attr(attrs, "src")
            self.current_comments[0]["author"]["image"] = src

    def handle_data(self, data):
        if self.current_attr == "name":
            self.current_comments[0]["author"]["scratchteam"] = data.endswith("*")
        elif self.current_attr == "content":
            self.current_comments[0]["content"] += html.escape(data).replace(
                "&#x27;", "&apos;"
            )

    def handle_endtag(self, tag):
        if tag == "li":
            self.current_comments[0]["content"] = re.sub(
                "\s+", " ", self.current_comments[0]["content"].strip()
            )
            if self.current_comments[0]["parent_id"] == None:
                self.comments.append(
                    ProfileComment(self.current_comments[0], self._user, self._client)
                )
            else:
                self.current_comments[-1]["replies"].append(
                    ProfileComment(self.current_comments[0], self._user, self._client)
                )
            self.current_comments.pop(0)

        if tag == "div" and self.current_attr:
            self.current_attr = None
        elif self.current_attr == "content":
            self.current_comments[0]["content"] += f"</{tag}>"


class SignatureParser(HTMLParser):
    def __init__(self, post_id):
        super().__init__()

        self.post_id = post_id
        self.correct_post = False
        self.in_signature = 0
        self.signature = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            current_class = get_attr(attrs, "class")
            if current_class and current_class.startswith("blockpost"):
                self.correct_post = get_attr(attrs, "id") == f"p{self.post_id}"
            elif self.correct_post and current_class == "postsignature":
                self.in_signature += 1
                return

        if self.in_signature > 0:
            self.signature += str.format(
                "<{0} {1}>", tag, " ".join(f'{key}="{value}"' for key, value in attrs)
            )
            if not tag in ("br", "hr"):
                self.in_signature += 1

    def handle_data(self, data):
        if self.in_signature > 0:
            self.signature += html.escape(data)

    def handle_endtag(self, tag):
        if tag == "div" and self.in_signature == 1:
            self.in_signature = 0
            self.correct_post = False
        elif self.in_signature > 0:
            self.signature += f"</{tag}>"
            if not tag in ("br", "hr"):
                self.in_signature -= 1


class HTMLToBBCodeParser(HTMLParser):
    smiles = {
        "smile": ":)",
        "neutral": ":|",
        "sad": ":(",
        "big_smile": ":D",
        "yikes": ":o",
        "wink": ";)",
        "hmm": ":/",
        "tongue": ":P",
        "lol": ":lol:",
        "mad": ":mad:",
        "roll": ":rolleyes",
        "cool": ":cool:",
    }

    formats = {
        "italic": "i",
        "bold": "b",
        "big": "big",
        "small": "small",
        "underline": "u",
        "strikethrough": "s",
    }

    def __init__(self):
        super().__init__()

        self.bbcode = ""
        self.close_tags = []
        self.in_quote = False

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.bbcode += "\n"
        elif tag == "img":
            src = get_attr(attrs, "src")
            if (
                re.search(
                    "//cdn\.scratch\.mit\.edu/scratchr2/static/__[a-z0-9]{32}__/djangobb_forum/img/smilies/[a-z_]{3,9}\.png",
                    src,
                )
                and src.split("smilies/")[1].split(".")[0] in self.smiles
            ):
                self.bbcode += smiles[src.split("smilies/")[1].split(".")[0]]
            else:
                self.bbcode += f"[img]{src}[/img]"
        elif tag == "span":
            current_class = get_attr(attrs, "class")
            if current_class and current_class.startswith("bb-"):
                self.bbcode += f"[{self.formats[current_class[3:]]}]"
                self.close_tags.insert(0, f"[/{self.formats[current_class[3:]]}]")
            elif get_attr(attrs, "style"):
                color = re.match("color:(.*)$", get_attr(attrs, "style")).groups()[0]
                if color.startswith("rgb"):
                    color = self.rgb_to_hex(rgb)

                self.bbcode += f"[color={color.upper()}]"
                self.close_tags.insert(0, f"[/color]")
        elif tag == "a":
            href = get_attr(attrs, "href")
            self.bbcode += f"[url={href}]"
            self.close_tags.insert(0, "[/url]")
        elif tag == "div":
            if get_attr(attrs, "style") == "text-align:center;":
                self.bbcode += "[center]"
                self.close_tags.insert(0, "[/center]")
            elif get_attr(attrs, "class") == "code":
                self.bbcode += "[code]\n"
                self.close_tags.insert(0, "[/code]\n")
        elif tag == "li":
            self.bbcode += "[*]"
        elif tag == "ul":
            self.bbcode += "[list]\n"
            self.close_tags.insert(0, "[/list]\n")
        elif tag == "ol":
            self.bbcode += "[list=1]\n"
            self.close_tags.insert(0, "[/list]\n")
        elif tag == "pre" and get_attr(attrs, "class") == "blocks":
            self.bbcode += "[scratchblocks]\n"
            self.close_tags.insert(0, "[/scratchblocks]\n")
        elif tag == "blockquote":
            self.bbcode += "[quote]\n"
            self.close_tags.insert(0, "[/quote]\n")
        elif tag == "p" and get_attr(attrs, "class") == "bb-quote-author":
            self.in_quote = True

    def handle_data(self, data):
        if self.in_quote:
            self.bbcode = self.bbcode[:-8] + f"[quote={data[:-7]}]\n"
            return

        self.bbcode += data

    def handle_endtag(self, tag):
        if tag in ("span", "a", "div", "li", "ul", "ol", "pre", "blockquote"):
            self.bbcode += self.close_tags[0]
            self.close_tags.pop(0)
        elif tag == "p" and self.in_quote:
            self.in_quote = False

    def rgb_to_hex(rgb):
        return "#" + "".join(
            hex(component)[2:]
            for component in re.match("rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb).groups()
        )


# For lack of a better name
class ScrapingSession:
    def __init__(self, client):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36."
        }
        self._client = client

    def get_follower_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(f"https://scratch.mit.edu/users/{username}/followers/", headers=self._headers).text

        return re.search("&raquo;\s+Followers\s+\((\d+)\)", page).groups()[0]

    def get_following_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(f"https://scratch.mit.edu/users/{username}/following/", headers=self._headers).text

        return re.search("&raquo;\s+Following\s+\((\d+)\)", page).groups()[0]

    def get_favorited_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(f"https://scratch.mit.edu/users/{username}/favorites/", headers=self._headers).text

        return re.search("&raquo;\s+Favorites\s+\((\d+)\)", page).groups()[0]

    def get_followed_studios_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(
            f"https://scratch.mit.edu/users/{username}/studios_following/",
            headers=self._headers
        ).text

        return re.search("&raquo;\s+Studios I Follow\s+\((\d+)\)", page).groups()[0]

    def get_curated_studios_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(f"https://scratch.mit.edu/users/{username}/studios/", headers=self._headers).text

        return re.search("&raquo;\s+Studios I Curate\s+\((\d+)\)", page).groups()[0]

    def get_shared_projects_count(self, user):
        username = user if isinstance(user, str) else user.username

        page = requests.get(f"https://scratch.mit.edu/users/{username}/projects/", headers=self._headers).text

        return re.search("&raquo;\s+Shared Projects\s+\((\d+)\)", page).groups()[0]

    def get_user_activity(self, user, max=100000):
        username = user if isinstance(user, str) else user.username

        page = requests.get(
            f"https://scratch.mit.edu/messages/ajax/user-activity/?user={username}&max={max}", 
            headers=self._headers
        ).text
        parser = ActivityParser()
        parser.feed(page)

        return parser.activities

    def get_profile_comments(self, user, all=False, page=1):
        username = user if isinstance(user, str) else user.username

        if all:
            comments = []

            while True:
                response = requests.get(
                    f"https://scratch.mit.edu/site-api/comments/user/{username}/?page={page}", 
                    headers=self._headers
                )

                if response.status_code == 404 or "<li" not in response.text:
                    return comments

                parser = ProfileCommentsParser(username, self._client)
                parser.feed(response.text)

                comments += parser.comments

                page += 1

        page_content = requests.get(
            f"https://scratch.mit.edu/site-api/comments/user/{username}/?page={page}",
            headers=self._headers
        ).text
        parser = ProfileCommentsParser(username, self._client)
        parser.feed(page_content)

        return parser.comments

    def get_signature(self, post_id, as_html=False):
        page_content = requests.get(
            f"https://scratch.mit.edu/discuss/post/{post_id}/",
            headers=self._headers
        ).text
        parser = SignatureParser(post_id)
        parser.feed(page_content)

        if not as_html:
            to_bbcode_parser = HTMLToBBCodeParser()
            to_bbcode_parser.feed(parser.signature)

            return to_bbcode_parser.bbcode[99:-29]

        return parser.signature
