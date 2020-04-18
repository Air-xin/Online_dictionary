"""
客户端
"""
from socket import *
import sys
import re


class MyDict():
    def __init__(self, tcp_sock):
        self.tcp_sock = tcp_sock

    # 用户信息输入
    def user_put(self):
        while True:
            print('请输入信息!')
            # 可能会强制退出
            try:
                name = input('name:')
                passwd = input('passwd:')
            except:
                self.tcp_sock.send(b'X ')
                self.tcp_sock.close()
                sys.exit()
            RE = r'\W+'
            data1 = re.findall(RE, name)
            data2 = re.findall(RE, passwd)
            # print(data1,data2)
            # 对输入规范进行判断
            if len(data1) or len(data2):
                print('请规范输入')
                continue
            else:
                msg = '%s %s' % (name, passwd)
                # print(msg)
                return msg

    # 注册
    def do_register(self):
        while True:
            data = self.user_put()
            msg = 'R %s' % data
            # 给服务端发送注册信息
            self.tcp_sock.send(msg.encode())
            response = self.tcp_sock.recv(1024).decode()
            # 对注册信息反馈做处理
            if response == 'YES':
                print('注册成功')
                # self.name = (data.split(' '))[0]
                self.do_query()
            else:
                print('注册失败')

    # 登录
    def do_login(self):
        while True:
            data = self.user_put()
            msg = 'I %s' % data
            # 给服务端发送登录信息
            self.tcp_sock.send(msg.encode())
            response = self.tcp_sock.recv(1024).decode()
            # 对登录信息反馈做处理
            if response == 'YES':
                print('登录成功')
                # self.name = (data.split(' '))[0]
                self.do_query()
            else:
                print('登录失败')

    # 单词查询
    def query_word(self):
        while True:
            try:
                word = input('请输入单词')
            except:
                self.tcp_sock.send(b'X ')
                self.tcp_sock.close()
                sys.exit()
            # 输入空，返回查询界面
            if not word:
                return
            data = 'Q %s' % (word)
            self.tcp_sock.send(data.encode())
            mean = self.tcp_sock.recv(2048).decode()
            print(mean)

    # 历史查询
    def query_hist(self):
        data = 'H '
        self.tcp_sock.send(data.encode())
        while True:
            mean = self.tcp_sock.recv(1024).decode()
            if mean == '##':
                return
            print(mean)

    # 查询界面
    def do_query(self):
        while True:
            print('输入：1 单词查询 --- 2 查看历史记录 --- 3 注销')
            # 可能会强制退出
            try:
                data = input('请输入选项：')
            except:
                self.tcp_sock.send(b'X ')
                self.tcp_sock.close()
                return
            # 单词查询
            if data == '1':
                self.query_word()
            # 查看历史记录
            elif data == '2':
                self.query_hist()
            # 注销,返回初始界面
            elif data == '3':
                self.start()
            # 输入选项有误
            else:
                print('请输入正确选项')

    # 初始界面
    def start(self):
        while True:
            print('输入：1 注册 --- 2 登录 --- 3 退出')
            # 可能会强制退出
            try:
                data = input('请输入选项：')
            except:
                self.tcp_sock.send(b'X ')
                self.tcp_sock.close()
                return
                # 注册
            if data == '1':
                self.do_register()
            # 登录
            elif data == '2':
                self.do_login()
            # 退出
            elif data == '3':
                self.tcp_sock.send(b'X ')
                sys.exit('谢谢使用')
            # 输入选项有误
            else:
                print('请输入正确选项')


# 启动函数
def main():
    ADDR = ('127.0.0.1', 8888)
    tcp_sock = socket()
    tcp_sock.connect(ADDR)
    MD = MyDict(tcp_sock)
    MD.start()


if __name__ == '__main__':
    main()
