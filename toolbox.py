import web
import os


def BASE_URL():
	if os.environ.get('PYTHONENV') == "production":
		return "http://git-full-ftp.herokuapp.com/"
	else:
		return "http://" + web.ctx.env.get('HTTP_HOST') + "/"


BASE_TITLE = "Git-full FTP"
VIEWS_DIR = 'templates/'
LAYOUT_NAME = 'layout'
render_engine = web.template.render(VIEWS_DIR, base=LAYOUT_NAME)


def render(view, data=None, title=''):
	if data is None:
		data = {}
	if title is '':
		title = BASE_TITLE
	else:
		title = title + " - " + BASE_TITLE

	data['title'] = title
	# data['base_url'] = BASE_URL
	# data['static_url'] = STATIC_URL
	return eval("render_engine." + str(view) + "(data)")
