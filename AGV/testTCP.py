import socket               # 导入 socket 模块
 
s = socket.socket()         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 1025                # 设置端口
s.bind((host, port))        # 绑定端口
 
s.listen(5)                 # 等待客户端连接
while True:
    # print(host)
    c,addr = s.accept()     # 建立客户端连接
    print('连接地址：', addr)
    data = c.recv(1024)  #接收数据
    print('recive:',data.decode()) #打印接收到的数据
    # c.send('欢迎访问菜鸟教程！')
    c.close()                # 关闭连接
