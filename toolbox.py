import os
import web


def BASE_URL():
	if os.environ.get('PYTHONENV') == "production":
		return "http://git-full-ftp.herokuapp.com/"
	else:
		return "http://localhost:8080/"


BASE_TITLE = "Git-full FTP"
VIEWS_DIR = 'templates/'
LAYOUT_NAME = 'layout'
render_engine = web.template.render(VIEWS_DIR, base=LAYOUT_NAME)



############################################
# Modifying web.py template rendering function to my old pattern
############################################
def render(view, data=None, title=''):
	if data is None:
		data = {}
	if title is '':
		title = BASE_TITLE
	else:
		title = title + " - " + BASE_TITLE

	data['title'] = title
	data['base_url'] = BASE_URL
	# data['static_url'] = STATIC_URL
	return eval("render_engine." + str(view) + "(data)")


##############################################
# Gives absolute path for path relative to executing script
##############################################
def absolute_path(*x):
	return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)



###################################
# Recursively delete directory on local machine
###################################
def delete_dir(abs_path):
	# shutil.rmtree(abs_path)

	for root, dirs, files in os.walk(abs_path):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			try:
				os.removedirs(os.path.join(root, name))
			except Exception:
				delete_dir(os.path.join(root, name))
				try:
					os.removedirs(os.path.join(root, name))
				except Exception:
					pass


######################
# Reverse string
######################
def reverse(string):
	return string[::-1]