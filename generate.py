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
INDEX_TEMPLATE = env.get_template('index.html')


def _convert_filename(filename, target='.html'):
	file, ext = os.path.splitext(filename)
	return '{}{}'.format(file, target)


def generate_context(attributes):
	context = {
		'title': attributes.get('title', SITE_TITLE),
		'author': attributes.get('author'),
		'category': attributes.get('category')
	}
	try:
		context.update({
			'date': datetime.date.strftime(attributes['date'], DATE_FORMAT)
		})
	except KeyError:
		pass
	return context



def get_all_posts():
	for entry in os.scandir(CONTENT_DIR):
		if all([
				not entry.name.startswith('.'),
				entry.name.endswith('.md'),
				entry.is_file()
			]):
				yield entry.name


def generate_html(filename, context, template=POST_TEMPLATE):
		new_file_name = _convert_filename(filename)
		open(os.path.join(OUTPUT_DIR, new_file_name), 'w').write(
			template.render(context)
		)


def parse_post(file, with_content=True):
	with open(os.path.join(CONTENT_DIR, file)) as f:
		whole_file = f.read()
	yaml_header, content = whole_file.split('---', maxsplit=1)
	attributes = yaml.load(yaml_header)
	if not with_content:
		return attributes
	return attributes, content


def generate_index(files):
	titles = [
		{
			'title': parse_post(file, with_content=False).get('title'),
			'url': _convert_filename(file)
		} for file in files
	]

	context = generate_context({})
	context.update({'posts': titles})
	generate_html('index.md', context, INDEX_TEMPLATE)


def main():
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)

	posts = get_all_posts()
	generate_index(posts)
	for post in posts:
		attributes, content = parse_post(post)
		content = misaka.html(content)
		context = generate_context(attributes)
		context.update({'content': content})
		generate_html(post, context, content)


if __name__ == '__main__':
	main()