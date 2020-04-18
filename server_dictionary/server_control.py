"""
服务端
"""
from socket import *
from multiprocessing import Process
from signal import *
import sys
from server_dictionary.server_model import *
from time import sleep

ADDR = ('127.0.0.1', 8888)


class MyProcess(Process):
    def __init__(self, tcp_connect, database):
        super().__init__()
        self.connect = tcp_connect
        self.database = database
        self.user_name = None

    # 处理用户注册
    def do_register(self, name, passwd):
        data = self.database.insert_user(name, passwd)
        # 判断用户是否存在,不存在为数据库添加用户,存在则拒绝
        if data == 'YES':
            self.user_name = name
            self.connect.send(data.encode())
        else:
            self.connect.send(data.encode())

    # 处理用户登录
    def do_login(self, name, passwd):
        data = self.database.select_user(name, passwd)
        # 判断用户密码是否正确,正确则允许,不正确则拒绝
        if data == 'YES':
            self.user_name = name
            self.connect.send(data.encode())
        else:
            self.connect.send(data.encode())

    # 处理用户单词查询
    def query_word(self, word):
        mean = self.database.select_word(self.user_name, word)
        # 判断用户查询单词是否存在，存在反馈用户单词解释，否则告知用户单词不存在
        if mean != '##':
            data = '%s : %s' % (word, mean)
            self.connect.send(data.encode())
        else:
            self.connect.send('单词不存在'.encode())

    # 处理用户历史记录查询
    def query_hist(self):
        data = self.database.select_hist(self.user_name)
        for i in data:
            msg = '%s\t%s' % i
            self.connect.send(msg.encode())
            sleep(0.1)
        self.connect.send(b'##')

    # 处理客户端请求
    def disponse(self):
        while True:
            # 接收客户请求
            data = self.connect.recv(1024).decode()
            msg = data.split(' ')
            # 处理用户退出
            if not data or msg[0] == 'X':
                self.connect.close()
                self.database.close()
                return
            if msg[0] == 'R':  # 注册
                self.do_register(msg[1], msg[2])
            elif msg[0] == 'I':  # 登录
                self.do_login(msg[1], msg[2])
            elif msg[0] == 'Q':  # 查询单词
                self.query_word(msg[1])
            elif msg[0] == 'H':  # 查询历史记录
                self.query_hist()

    def run(self):
        self.database.cursor()
        self.disponse()


# 启动函数
def main():
    signal(SIGCHLD, SIG_IGN)
    database = MyDatabase()
    # 创建tcp套接字
    tcp_sock = socket()
    tcp_sock.bind(ADDR)
    tcp_sock.listen(3)
    # 循环监听客户链接
    while True:
        try:
            tcp_connect, addr = tcp_sock.accept()
            print('客户端链接：', addr)
        except:
            tcp_sock.close()
            sys.exit('服务器退出')
        # 为客户端处理请求
        p = MyProcess(tcp_connect, database)
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
