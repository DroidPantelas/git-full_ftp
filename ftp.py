import ftplib
import os

class synchronizer():
    def __init__(self, ftp_host, ftp_port, ftp_user, ftp_pass, local_dir, remote_dir):
        self.ftp_host = ftp_host
        self.ftp_port = ftp_port
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.local_dir = local_dir
        self.remote_dir = remote_dir
        self.connection = ftplib.FTP()
    #####################################################
    # Class initiailized with FTP server paramaters and local directory
    #####################################################


    #######################
    # Remove trailing slash
    #######################
    def stripslashes(self, string):
        if string is "":
            return string
        if string[-1] is "/":
            return string[:-1]
        else:
            return string


    ########################
    # Remove empty elements in array
    ########################
    def remove_empty(self, array):
        count = 0
        for elem in array:
            if not elem:
                del array[count]
            count = count + 1
        return array


    ########################
    # Connect to FTP server and login
    ########################
    def connect(self):
        self.connection.connect(self.ftp_host, self.ftp_port)
        self.connection.login(self.ftp_user, self.ftp_pass)



    ###################################
    # Check if remote object is a directory
    ###################################
    def is_dir(self, dirname):
        current = self.connection.pwd()
        try:
            self.connection.cwd(dirname)
            is_dir = True
            self.connection.cwd(current)
        except Exception:
            is_dir = False

        return is_dir



    ######################################
    # Recursively delete remote directory
    ########################################
    def delete_dir(self, dirname):
        current = self.connection.pwd()
        try:
            self.connection.rmd(dirname)
        except Exception:
            self.connection.cwd(dirname)
            for elem in self.connection.nlst():
                try:
                    self.connection.delete(elem)
                except Exception:
                    try:
                        self.connection.rmd(elem)
                    except Exception:
                        self.delete_dir(elem)

            self.connection.cwd(current)
            self.connection.rmd(dirname)




    #############################
    # Upload local directory to remote
    #############################
    def sync(self):
        self.connect()  # connect


        #### navigate to remote destination 
        remote_current = self.connection.pwd()

        dest_remote = self.remote_dir
        dest_remote = dest_remote.replace(remote_current, "", 1)
        dest_remote = self.stripslashes(dest_remote)
        self.connection.cwd(dest_remote)
        #################################################
        # remote working directory = REMOTE DESTINATION
        ###############################################


        ###################################
        # Commence os.walk and transfer
        # os.walk is a way to cover all the files and directories
        # on local machine recursively
        ###################################
        for case in os.walk(self.local_dir):
            path = case[0]      # absolute path
            dirs = case[1]      # directories in the directory
            files = case[2]     # files in the direcotry


            ############################################
            # relative_path is the path of the directory
            # currently running in the os.walk on the
            # remote server relative to remote_dir
            ############################################
            relative_path = self.stripslashes(path.replace(self.stripslashes(self.local_dir), "", 1))

            self.connection.cwd(self.remote_dir + relative_path)    # Change working directory to dir in os.walk


            ###########################################
            # Make all the directories in current folder
            # on remote. Files in those directories will
            # be transferred as we sail through os.walk
            ##########################################
            for directory in dirs:
                try:
                    self.connection.mkd(directory)
                except Exception:
                    pass        # If directory exists, program will hit the error and not create new

            ########################################
            # Upload all the files in current directory.
            # As we sail through os.walk, we cover all
            # the directories and upload the files in them.
            #############################################
            for f in files:
                try:
                    self.connection.delete(f)
                except Exception:
                    pass    # If file exists, program will delete it. Else hit error.

                # Upload file
                self.connection.storbinary("STOR " + f, open(path + "/" + f, "rb"))

            #### Files uploaded

            ##############################
            # Those files and dirs which are
            # not on local but are on remote
            # will be deleted
            ##############################
            for elem in self.connection.nlst():
                ###############################
                # Elem is every dir+file on remote
                ###############################
                if elem == "." or elem == "..":
                    continue
                if self.is_dir(elem) and (not elem in dirs):            # If remote is dir, and not present on local
                    self.delete_dir(elem)
                elif (not self.is_dir(elem)) and (not elem in files):   # If remote is file, and not present on local
                    self.connection.delete(elem)
