import web
from toolbox import *

urls = (
	"/", "index"
)


class index:
	def GET(self):
		return render("index")

if __name__ == "__main__": 
	app = web.application(urls, globals())
	app.run()
