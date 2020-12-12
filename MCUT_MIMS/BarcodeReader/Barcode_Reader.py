import time
import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
import socket

productNum = ['01234567S', '安瓿瓶', 500]

def settup_socket():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname() 
    port = 1025                
    print('Host name:', host)
    # s.bind((host, port))       # for windows
    s.bind(('', port)) 

    return s

def app(serial_num):
    window = tk.Tk()
    window.config(bg = '#323232')
    # ft_title = Font(family='Times new Roman', size=24, weight = 'bold')
    ft_article = Font(size=24 )
    window.attributes("-topmost", 1) # Stick the window
    window.focus_force()
    window.title('Barcode Result')

    windowSize = [720, 1280]
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (windowSize[0]/2)
    y = (hs/2) - (windowSize[1]/2)
    window.geometry('%dx%d+%d+%d' % (windowSize[0], windowSize[1], x, y))

    header_label = tk.Label(window, text = 'Product Info', font=ft_article, bg='#323232', fg='#ffffff')
    header_label.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()

    img = Image.open('/home/pi/Desktop/QRcode_new/IMG.jpg')
    img = img.resize((450, 360), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image = img)
    panel.image = img
    panel.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()

    result_label = tk.Label(window, bg='#323232')
    result_label.pack()

    height_frame = tk.Frame(window)
    # 向上對齊父元件
    height_frame.pack(side=tk.TOP)
    height_label = tk.Label(height_frame, text='產品名稱: %s' %(serial_num[1]), font=ft_article, bg='#323232', fg='#ffffff')
    height_label.pack(side=tk.LEFT)

    # 以下為 weight_frame 群組
    weight_frame = tk.Frame(window)
    weight_frame.pack(side=tk.TOP)
    weight_label = tk.Label(weight_frame, text='產品編號: %s' %(serial_num[0]), font=ft_article, bg='#323232', fg='#ffffff')
    weight_label.pack(side=tk.LEFT)
    
    # 以下為 weight_frame 群組
    weight_frame = tk.Frame(window)
    weight_frame.pack(side=tk.TOP)
    weight_label = tk.Label(weight_frame, text='產品數量: %s' %(serial_num[2]), font=ft_article, bg='#323232', fg='#ffffff')
    weight_label.pack(side=tk.LEFT)

    # 以下為 weight_frame 群組
    time_frame = tk.Frame(window)
    time_frame.pack(side=tk.TOP)
    time_frame = tk.Label(time_frame, text='入庫時間: %s' %(time.ctime()), font=ft_article, bg='#323232', fg='#ffffff')
    time_frame.pack(side=tk.LEFT)

    result_label = tk.Label(window, bg='#323232')
    result_label.pack()

    check_frame = tk.Frame(window)
    check_frame.pack(side=tk.TOP)
    check_frame = tk.Label(check_frame, text='成功入庫!', font=ft_article, bg='#323232', fg='#ffff66')
    check_frame.pack(side=tk.LEFT)
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()
    
    result_label = tk.Label(window, bg='#323232')
    result_label.pack()
    
    numIdx = 32 # gif的帧数
    # 填充6帧内容到frames
    frames = [tk.PhotoImage(file='tenor1.gif', format='gif -index %i' %(i)) for i in range(numIdx)]

    def update(idx): # 定时器函数
        frame = frames[idx]
        idx += 1 # 下一帧的序号：在0,1,2,3,4,5之间循环(共6帧)
        label.configure(image=frame) # 显示当前帧的图片
        window.after(50, update, idx%numIdx) # 0.1秒(100毫秒)之后继续执行定时器函数(update)

    label = tk.Label(window)
    label.pack()
    window.after(0, update, 0) # 立即启动定时器函数(update)

    window.after(8000, lambda: window.destroy()) # Destroy the widget after 30 seconds

    window.mainloop()

def main():
    s = settup_socket()
    s.listen(5)

    while True:
        c,addr = s.accept()     
        print('recive from address', addr)
        data = c.recv(1024)  
        data = data.decode()
        print('recived data:',data)
        data = data.split(',')
        # c.send('hello world')
        c.close()
        if data[0] == productNum[0]:
            app(serial_num=productNum)
main()