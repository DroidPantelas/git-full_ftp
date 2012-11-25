import web
import urllib2
from toolbox import *
from encrypter import *

# encrypter.py not included in git repository due to security reasons.
# If you want to make changes to this app, make encrypter.py which has following functions
# a) get_url_params(data)
#       data = dictionary with keys -> ftp, dir, zip and corresponding values
#       return dictionary with keys -> uid, access_key, code with corresponding values


urls = (
    "/", "index",
    "/add/?", "add",
    "/sync/?", "sync"
)
base_url = BASE_URL()


class index:
    def GET(self):
        return render("index")


class add:
    def POST(self):
        data = web.input()
        params = get_url_params(data)

        url = base_url + "sync?uid=" + params["uid"] + "&access_key=" + params["access_key"] + "&code=" + params['code']

        return render("index", {"url": url})


class sync:
    def GET(self):
        data = web.input()
        config = get_data(data)

        buff = urllib2.urlopen(config['zip'])
        f = open(absolute_path("tmp/" + (config['zip'].split("/")).pop()), "wb")
        f.write(buff.read())
        f.close()

        return data['uid']


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
