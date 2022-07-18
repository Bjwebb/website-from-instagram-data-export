import json
import os
import shutil
import subprocess

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)

with open("exported_json/content/posts_1.json") as fp:
    posts = json.load(fp)


for post in posts:
    if len(post["media"]) == 1:
        for key in ["title", "creation_timestamp"]:
            post[key] = post["media"][0][key]
    for media in post["media"]:
        os.makedirs(os.path.join("out", os.path.dirname(media["uri"])), exist_ok=True)
        original_file = os.path.join("exported_json", media["uri"])
        copied_file = os.path.join("out", media["uri"])
        media["thumb_uri"] = media["uri"] + ".thumb.jpg"
        if False:
            shutil.copy(original_file, copied_file)
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    original_file,
                    "-vf",
                    "scale=320:320:force_original_aspect_ratio=decrease",
                    "-vframes",
                    "1",
                    os.path.join("out", media["thumb_uri"]),
                ],
                check=True,
            )
    with open(
        os.path.join("out", f"post_{post['creation_timestamp']}.html"), "w"
    ) as fp:
        template = env.get_template("post.html")
        fp.write(template.render(post=post))

posts.sort(key=lambda post: -post["creation_timestamp"])

with open(os.path.join("out", "index.html"), "w") as fp:
    template = env.get_template("index.html")

    fp.write(template.render(posts=posts))
