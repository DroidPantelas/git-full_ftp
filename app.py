import web                      # web.py framework
import urllib2                  # for downloading repo zip file
from toolbox import *           # supporting functions
from encrypter import *         # URL encrypter
import zipfile                  # to extract zip file
from ftp import synchronizer    # ftp transfer
import os                       # directory navigation

#############################################################################
#############################################################################
# encrypter.py not included in git repository due to security reasons.
# If you want to make changes to this app, make encrypter.py which has following functions
# a) get_url_params(data)
#       data = dictionary with keys -> ftp, dir, zip and corresponding values
#       return dictionary with keys -> uid, access_key, code with corresponding values
# 
# b) get_data(data)
#       data = dictionary with keys -> uid, access_key, code with corresponding values
#       return dictionary with keys -> ftp, dir, zip and corresponding values
#############################################################################
#############################################################################


urls = (
    "/", "index",
    "/add/?", "add",
    "/sync/?", "sync"
)
base_url = BASE_URL()  ### Root URL of the WebApp


### Front page
class index:
    def GET(self):
        return render("index")


### Generate URL from posted data
class add:
    def POST(self):
        data = web.input() # post data
        params = get_url_params(data)   # get the encrypter URL parameter from encrypter.py

        url = base_url + "sync?uid=" + params["uid"] + "&access_key=" + params["access_key"] + "&code=" + params['code']
        ### Sync URL

        return render("index", {"url": url})


class sync:
    def GET(self):
        data = web.input()  # GET data
        config = get_data(data) # Get the decrypter server and git config from encrypter.py

        ############
        # Downloading the zip file of the repo
        ##############

        buff = urllib2.urlopen(config['zip'])
        f = open(absolute_path("tmp/" + (config['zip'].split("/")).pop()), "wb") #### Writing it to tmp/master.zip
        f.write(buff.read())
        f.close()

        ###########
        # Download finished
        ###########


        ###########
        # Extract the zipfile to same folder
        ###########

        repo = zipfile.ZipFile(absolute_path("tmp/" + (config['zip'].split("/")).pop()))
        repo.extractall(absolute_path("tmp/"))
        local_dirname = repo.filelist[0].filename.replace("/","")
        repo.close()
        os.remove(absolute_path("tmp/" + (config['zip'].split("/")).pop()))
        
        ###########
        # Extraction finished. Zip file deleted.
        ############

        ##################
        # Getting username, password, host, port from FTP_URL
        ##################

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

        ##### End



        ##############
        # Synchronize
        ##############

        s = synchronizer(host, port, username, password, absolute_path("tmp/" + local_dirname), config['dir'])
        s.sync()

        #### Done


        #### Delete the extracted directory
        delete_dir(absolute_path("tmp/" + local_dirname))

        return data['uid']


        def POST(self):
            data = web.input()  # GET data
            config = get_data(data) # Get the decrypter server and git config from encrypter.py

            ############
            # Downloading the zip file of the repo
            ##############

            buff = urllib2.urlopen(config['zip'])
            f = open(absolute_path("tmp/" + (config['zip'].split("/")).pop()), "wb") #### Writing it to tmp/master.zip
            f.write(buff.read())
            f.close()

            ###########
            # Download finished
            ###########


            ###########
            # Extract the zipfile to same folder
            ###########

            repo = zipfile.ZipFile(absolute_path("tmp/" + (config['zip'].split("/")).pop()))
            repo.extractall(absolute_path("tmp/"))
            local_dirname = repo.filelist[0].filename.replace("/","")
            repo.close()
            os.remove(absolute_path("tmp/" + (config['zip'].split("/")).pop()))
            
            ###########
            # Extraction finished. Zip file deleted.
            ############

            ##################
            # Getting username, password, host, port from FTP_URL
            ##################

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

            ##### End



            ##############
            # Synchronize
            ##############

            s = synchronizer(host, port, username, password, absolute_path("tmp/" + local_dirname), config['dir'])
            s.sync()

            #### Done


            #### Delete the extracted directory
            delete_dir(absolute_path("tmp/" + local_dirname))

            return data['uid']

if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()
