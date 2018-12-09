import os

import misaka


BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def get_all_posts():
	for entry in os.scandir(CONTENT_DIR):
		if all([
				not entry.name.startswith('.'),
				entry.name.endswith('.md'),
				entry.is_file()
			]):
			yield entry.name


def generate_html(files):
	for file in files:
		with open(os.path.join(CONTENT_DIR, file)) as f:
			content = misaka.html(f.read())
			new_file_name = os.path.splitext(file)[0] + '.html'
			open(os.path.join(OUTPUT_DIR, new_file_name), 'w').write(content)

def main():
	if not os.path.exists(OUTPUT_DIR):
		os.mkdir(OUTPUT_DIR)

	generate_html(get_all_posts())


if __name__ == '__main__':
	main()