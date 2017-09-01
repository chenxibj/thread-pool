# -*- coding:utf-8 -*- 
import paramiko
import logging
logger = logging.getLogger(__name__)
res = {"status":1,"msg":"success"}

class SshWrapper(object):
    def __init__(self, host_ip, username="root", private_key="/home/admin/.ssh/id_rsa"):
        self._host_ip = host_ip
        self._username = username
        self._private_key = private_key
        self._sshcon = None
        self._sftp = None
        self.__connect()

    def __connect(self):
        #try:
        sshcon = paramiko.SSHClient()
        sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshcon.connect(hostname=self._host_ip, port=80,username=self._username, key_filename=self._private_key)
        self._sshcon = sshcon
        #except  Exception as e:
        #    logger.info("%s connect fail: %s" % (self._host_ip,e))
        #   raise ConnectException("%s connect fail: %s" % (self._host_ip,e))

    def execCommand(self, command, log=None):
        if log:
            stdin, stdout, stderr = self._sshcon.exec_command("tail -n 500 %s" % log)
        else:
            stdin, stdout, stderr = self._sshcon.exec_command(command)
        data = stdout.read()
        err = stderr.read()
        self.__close()
        code = stdout.channel.recv_exit_status()
        if code != 0:
            res["status"] = 0
            res["msg"] = err.strip()
            logger.info("command exec result: %s" % res) 
        return res
        
    def downloadFile(self, remote_path, local_path):
        if self._sftp is None:
            st = self._sshcon.get_transport()
            self._sftp = paramiko.SFTPClient.from_transport(st)
        self._sftp.get(remote_path, local_path)
        self.__close()

    def putFile(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._sshcon)
        self._sftp.put(localpath, remotepath)
        self.__close()

    def __close(self):
        if self._sshcon:
            self._sshcon.close()
        if self._sftp:
            self._sftp.close()
            
if __name__ == "__main__":
    ssh = SshWrapper("172.27.33.32","root","/root/.ssh/id_rsa")
    ssh.execCommand("ls /root/.ssh/")