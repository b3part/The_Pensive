import datetime
import os

from jinja2 import Template, Environment, FileSystemLoader

import misaka
import yaml


BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
THEME_DIR = os.path.join(BASE_DIR, 'theme')
SITE_TITLE = "Hello World!"

DATE_FORMAT = '%Y-%m-%d'


env = Environment(loader=FileSystemLoader(THEME_DIR))
POST_TEMPLATE = env.get_template('post.html')


def generate_context(attributes):
	return {
		'title': attributes['title'] or SITE_TITLE,
		'date': datetime.date.strftime(attributes['date'], DATE_FORMAT),
		'author': attributes['author'] or None,
		'category': attributes['category'] or None
	}


def get_all_posts():
	for entry in os.scandir(CONTENT_DIR):
		if all([
				not entry.name.startswith('.'),
				entry.name.endswith('.md'),
				entry.is_file()
			]):
				yield entry.name


def generate_html(filename, context, post):
		new_file_name = os.path.splitext(filename)[0] + '.html'
		context.update({'content': post})
		open(os.path.join(OUTPUT_DIR, new_file_name), 'w').write(
			POST_TEMPLATE.render(context)
		)


def parse_post(file):
	with open(os.path.join(CONTENT_DIR, file)) as f:
		whole_file = f.read()
	yaml_header, content = whole_file.split('---', maxsplit=1)
	attributes = yaml.load(yaml_header)
	return attributes, content


def main():
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)

	posts = get_all_posts()
	for post in posts:
		attributes, content = parse_post(post)
		content = misaka.html(content)
		context = generate_context(attributes)
		generate_html(post, context, content)


if __name__ == '__main__':
	main()