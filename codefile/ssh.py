# import paramiko
#
# #创建ssh对象
# ssh=paramiko.SSHClient()
#
# #允许连接不在know_host文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# #连接服务器
# ssh.connect(hostname='ip',port=22,username='user',password='user')
#
# #执行命令
# stdin,stdout,stderr=ssh.exec_command('ls')
#
# #获取命令结果
# result=stdout.read()
# print(result)
#
# #关闭连接
# ssh.close()


#连接服务器上传下载
#import paramiko

# transport=paramiko.Transport(('ip',22))
# transport.connect(username='user',password='user')
# sftp=paramiko.SFTPClient.from_transport(transport)
#
# #将文件上传至服务器
# local_path='/Users/wjb/test'
# remote_path='/home/ngs/wjb_test'
# sftp.put(local_path,remote_path)
#
# #从服务器下载文件
# sftp.get(remote_path,local_path)
#
# transport.close()



#从服务器上下载整个目录
#函数式

import os
import stat
import paramiko

def get_files(sftp,remote_dir):

    files=sftp.listdir_attr(remote_dir)

    file_list=[]
    for file in files:
        filename=remote_path+data+'/'+file.filename
        if stat.S_ISDIR(file.st_mode):
            file_list.extend(get_files(sftp,filename))
        else:
            file_list.append(filename)

    return file_list

if __name__=='__main__':

    remote_path='/DataCenter/CleanData/'
    data='180813HZ02_M04057_0338_000000000-C26PT'
    remote_dir=remote_path+data

    transport=paramiko.Transport(('ip',22))
    transport.connect(username='user',password='user')
    sftp=paramiko.SFTPClient.from_transport(transport)

    filenames=get_files(sftp,remote_dir)
    local_dir='/Users/wjb/Desktop/180813HZ02_M04057_0338_000000000-C26PT'
    for file in filenames:
        local_file=os.path.join(local_dir,file.split('/')[-1])

        print(file)
        print('######')
        print(local_file)
        sftp.get(file,local_file)

#OOP(面向对象）

class RemoteServer(object):
    def __init__(self,ip,username,password):
        self.ip=ip
        self.username=username
        self.password=password

    def connect(self):
        pass

    def close(self):
        pass

    def send(self,cmd):
        pass

    #get单个文件
    def sftp_get(self,remote_file,local_file):
        t=paramiko.Transport((self.ip,22))
        t.connect(username=self.username,password=self.password)
        sftp=paramiko.SFTPClient.from_transport(t)
        sftp.get(remote_file,local_file)
        t.close()

    #put单个文件
    def sftp_put(self,local_file,remote_file):
        t = paramiko.Transport((self.ip, 22))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_file, remote_file)
        t.close()

if __name__=='__main__':
    remote_file=r'/home/ngs/test.txt'
    local_file=r'/Users/wjb/test.txt'

    host=RemoteServer('ip','user','user')
    #从服务器上下载文件
    #host.sftp_get(remote_file,local_file)

    #从本地上传文件到服务器
    host.sftp_put(local_file,remote_file)


