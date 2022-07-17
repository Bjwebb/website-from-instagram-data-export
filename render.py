import json

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."), autoescape=True)

template = env.get_template("template.html")

with open("exported_json/content/posts_1.json") as fp:
    posts = json.load(fp)

for post in posts:
    if len(post["media"]) == 1:
        for key in ["title", "creation_timestamp"]:
            post[key] = post["media"][0][key]

posts.sort(key=lambda post: post["creation_timestamp"])

with open("out.html", "w") as fp:
    fp.write(template.render(posts=posts))
