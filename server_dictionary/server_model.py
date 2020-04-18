"""
服务端数据库
"""
import pymysql


class MyDatabase:
    def __init__(self):
        # 链接数据库并生成对象
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  database='dict',
                                  charset='utf8')

    # 创建数据库游标
    def cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库游标
    def close(self):
        self.cur.close()

    # 注册,添加用户
    def insert_user(self, name, passwd):
        sql = 'select name from user where name=%s;'
        self.cur.execute(sql, [name])
        msg = self.cur.fetchone()
        # 查看数据库中,用户是否存在
        if msg:
            return 'NO'
        else:
            sql = 'insert into user(name,passwd) values (%s,%s);'
            try:
                self.cur.execute(sql, [name, passwd])
                self.db.commit()
            except:
                self.db.rollback()
                return 'NO'
            return 'YES'

    # 登录
    def select_user(self, name, passwd):
        sql = 'select name from user where name=%s and passwd=%s;'
        self.cur.execute(sql, [name, passwd])
        msg = self.cur.fetchone()
        # 查看数据库中,用户密码是否正确
        if msg:
            return 'YES'
        else:
            return 'NO'

    # 查询单词
    def select_word(self, name, word):
        sql = 'select mean from words where word=%s'
        self.cur.execute(sql, [word])
        mean = self.cur.fetchone()
        # 查看数据库是否有该单词
        if mean:
            self.insert_hist(name, word)
            return mean[0]
        else:
            return '##'

    # 插入查询历史
    def insert_hist(self, name, word):
        # 查看用户id
        sql = 'select id from user where name=%s;'
        self.cur.execute(sql, [name])
        id = self.cur.fetchone()
        # 为用户添加历史记录
        sql = 'insert into hist(word,u_id) values (%s,%s);'
        try:
            self.cur.execute(sql, [word, id])
            self.db.commit()
        except:
            self.db.rollback()

    # 查询历史
    def select_hist(self, name):
        sql = 'select time,word from hist left join user on u_id=user.id where name=%s order by time desc limit 10;'
        self.cur.execute(sql, [name])
        data = self.cur.fetchall()
        return data
