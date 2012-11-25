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

    def stripslashes(self, string):
        if string is "":
            return string
        if string[-1] is "/":
            return string[:-1]
        else:
            return string

    def remove_empty(self, array):
        count = 0
        for elem in array:
            if not elem:
                del array[count]
            count = count + 1
        return array

    def connect(self):
        self.connection.connect(self.ftp_host, self.ftp_port)
        self.connection.login(self.ftp_user, self.ftp_pass)

    def sync(self):
        self.connect()

        remote_current = self.connection.pwd()

        dest_remote = self.remote_dir
        dest_remote = dest_remote.replace(remote_current, "", 1)
        dest_remote = self.stripslashes(dest_remote)
        self.connection.cwd(dest_remote)

        ##########
        # Commence os.walk and transfer
        ##########
        print(self.local_dir)
        for case in os.walk(self.local_dir):
            path = case[0]
            print(path)
            dirs = case[1]
            files = case[2]

            relative_path = self.stripslashes(path.replace(self.stripslashes(self.local_dir), "", 1))
            # slashes = relative_path.count("/")
            # directories = relative_path.split("/")

            self.connection.cwd(self.remote_dir + relative_path)

            for directory in dirs:
                try:
                    self.connection.mkd(directory)
                except Exception:
                    pass        # If directory exists, program will hit the error and not create new

            for f in files:
                try:
                    self.connection.delete(f)
                except Exception:
                    pass    # If file exists, program will delete it. Else hit error.

                self.connection.storbinary("STOR " + f, open(path + "/" + f, "rb"))

            for elem in self.connection.nlst():
                if self.is_dir(elem) and (not elem in dirs):
                    # self.connection.rmd(elem)
                    self.delete_dir(elem)
                elif (not self.is_dir(elem)) and (not elem in files):
                    self.connection.delete(elem)


    def is_dir(self, dirname):
        current = self.connection.pwd()
        try:
            self.connection.cwd(dirname)
            is_dir = True
            self.connection.cwd(current)
        except Exception:
            is_dir = False

        return is_dir


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
                    self.delete_dir(elem)

        self.connection.cwd(current)
        self.connection.rmd(dirname)
