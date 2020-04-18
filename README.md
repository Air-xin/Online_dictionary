在线词典
1. 需求功能分析
    确定要实现的功能
    需要保存的数据 : 用户信息   单词信息   历史记录信息
2. 技术分析
     * 使用什么并发模型   Process多进程
     * 网络 --> tcp
     * 两个界面相互怎么跳转 (写一个demo示例)
     * 存储 --> 数据库 dict
         还需要什么表,并且创建出来
         words -->  id   word  mean
         user --> id  name  passwd
         create table user (id int primary key auto_increment,name varchar(30) not null,passwd char(64) not null);
         history --> id  word  time  user_id
         create table hist (id int primary key auto_increment,word varchar(30),time datetime default now(),user_id int,constraint user_fk foreign key (user_id) references user(id));
         (history -->  id  name  word  time)
3. 功能模块和封装
     功能分为那些模块
      * 多进程tcp网络并发结构
      * 注册
      * 登录
      * 查单词
      * 历史记录
      * 注销退出
     封装 --> mvc
     m -->  数据模型
     v -->  视图模型
     c -->  控制模型
     客户端模块  :   请求数据,为用户打印结果    v
     服务端    逻辑控制  接收请求,回发数据     c
              数据处理  得到c的指令,进行数据查找交互    m
4. 通信协议
     设计通信
                      请求类型     请求内容
      * 注册            R         name   passwd
      * 登录            L
      * 查单词          Q
      * 历史记录        H
      * 注销退出        E
5. 具体的模块逻辑
      * 多进程tcp网络并发结构 和 数据库交互办法
      * 注册
           客户端 :  输入用户名密码
                    将用户名密码发送给服务端
                    等待反馈
                    Yes --> 注册整个
                    No --> 停留在一级界面
           服务端 : 接收请求
                   判断是否可以注册
                   给客户端反馈
                   YES --> 将用户信息插入数据库
                   No -->
      * 登录
      * 查单词
      * 历史记录
      * 注销退出
6. 优化完善
    * 代码重构
    * 添加图形化界面操作
    * 密码存储加密