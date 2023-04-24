import markdown
import os
import yaml
from jinja2 import Environment, FileSystemLoader

posts = []


def generate_html(directory, template, jinja_env):
    html_template = jinja_env.get_template(template)
    for file in os.listdir(directory):
        if file.endswith(".md"):
            with open(os.path.join(directory, file), "r") as md_file:
                content = md_file.read()
            yaml_content, md_content = content.split("---")[1:]
            yaml_var = yaml.safe_load(yaml_content)
            if directory == "posts":
                posts.append(yaml_var)
            output_file = os.path.join("html", file.replace(".md", ".html"))
            with open(output_file, "w") as output:
                output.write(html_template.render(**yaml_var, content=markdown.markdown(md_content), posts=posts))


def main():
    jinja_env = Environment(loader=FileSystemLoader("templates"))

    for directory, template in [("posts", "post.html"), ("pages", "page.html"), ("home", "index.html")]:
        generate_html(directory, template, jinja_env)


if __name__ == '__main__':
    main()
