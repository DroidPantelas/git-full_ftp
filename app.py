import web
import urllib2
from toolbox import *
from encrypter import *
import zipfile
from ftp import synchronizer
import os

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

        repo = zipfile.ZipFile(absolute_path("tmp/" + (config['zip'].split("/")).pop()))
        repo.extractall(absolute_path("tmp/"))
        local_dirname = repo.filelist[0].filename.replace("/","")
        repo.close()
        os.remove(absolute_path("tmp/" + (config['zip'].split("/")).pop()))

        ftp_url = config['ftp']
        url = ftp_url.replace("ftp://","")
        if url[-1] == "/":
            url = url[:-1]

        tmp1 = url.split(":",1)
        username = tmp1[0]
        tmp2 = reverse(tmp1[1]).split("@",1)
        password = reverse(tmp2.pop())
        host_port = reverse(tmp2[0])
        host, port = host_port.split(":")

        s = synchronizer(host, port, username, password, absolute_path("tmp/" + local_dirname), config['dir'])
        s.sync()

        delete_dir(absolute_path("tmp/" + local_dirname))

        return data['uid']


if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
