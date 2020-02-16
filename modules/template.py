import pathlib
path = str(pathlib.Path(__file__).parents[1])

def get_template(content:list):
	template_html = open(path + '/template/mail.html', 'r').read()
	album_html = open(path + '/template/mail_release.html', 'r').read()

	nb_releases = str(len(content))

	releases_html = ''
	for album in content:
		html = album_html
		html = html.replace('{{ALBUM_IMG}}', album['cover_medium'])
		html = html.replace('{{ALBUM_TITLE}}', album['title'])
		html = html.replace('{{ALBUM_LINK}}', album['link'])
		html = html.replace('{{ALBUM_ARTIST}}', album['artist']['name'])
		releases_html += html

	template_html = template_html.replace('{{NB_RELEASES}}', nb_releases)
	template_html = template_html.replace('{{RELEASES}}', releases_html)

	return template_html
