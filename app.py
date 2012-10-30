import web

urls = (
	"/", "index"
)

BASE_URL = "http://localhost:8080/"
STATIC_URL = "http://localhost:8080/static/"
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
		title = title + " | " + BASE_TITLE

	data['title'] = title
	data['base_url'] = BASE_URL
	data['static_url'] = STATIC_URL
	return eval("render_engine." + str(view) + "(data)")


class index:
	def GET(self):
		return render("index")

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.run()
