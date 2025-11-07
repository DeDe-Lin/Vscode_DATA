import tkinter as tk
import shutil

root = tk.Tk()   # 建立 tkinter 視窗物件
root.title('搬移工具')        # 設定標題
width = 600
height = 400
left = 0
top = 0
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置
root.configure(background='#53cf5d')  

testtex = tk.StringVar()
input1 = tk.StringVar()
input2 = tk.StringVar()

testtex.set("錯誤訊息顯示區")
def function_copy():
    import traceback, os
    f1 = input1.get().strip()
    f2 = input2.get().strip()
    if not f1 or not f2:
        testtex.set("請填入來源與目標路徑")
        return
    try:
        shutil.copytree(f1, f2, copy_function=shutil.copy2, dirs_exist_ok=True)
        testtex.set(f"已複製：{f1} -> {f2}")
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)  # 在終端查看完整錯誤
        testtex.set(f"複製錯誤：{e}")

def function_move():
    import traceback, os
    f1 = input1.get().strip()
    f2 = input2.get().strip()
    if not f1 or not f2:
        testtex.set("請填入來源與目標路徑")
        return
    try:
        shutil.copytree(f1, f2, copy_function=shutil.move, dirs_exist_ok=True)
        testtex.set(f"已搬移：{f1} -> {f2}")
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        testtex.set(f"搬移錯誤：{e}")


frame1 = tk.Frame(root, pady=10, padx=10, bg='#c90')   # 第一個 Frame 元件
frame2 = tk.Frame(root, pady=10, padx=10, bg='#09c')   # 第二個 Frame 元件
frame3 = tk.Frame(root, pady=10, padx=10, bg='#9c0')   # 第二個 Frame 元件
frame4 = tk.Frame(root, pady=10, padx=10, bg='#0c9')   # 第二個 Frame 元件


tk.Label(frame1,text='請輸入移動前位置：').pack(side='left')
tk.Entry(frame1,textvariable=input1,width=50,borderwidth=5).pack(side='left',padx=10)
tk.Label(frame2,text='請輸入移動後位置：').pack(side='left')
tk.Entry(frame2,textvariable=input2,width=50,borderwidth=5).pack(side='left',padx=10)
tk.Button(frame3, text='複製',font=('微軟正黑體',20,'bold'),width=4,height=1,activeforeground='#f00',command=function_copy).pack(side='left',padx=20)
tk.Button(frame3, text='搬移',font=('微軟正黑體',20,'bold'),width=4,height=1,activeforeground='#f00',command=function_move).pack(side='left',padx=20)
tk.Label(frame4,textvariable=testtex).pack(side='left')


tk.Label(root, text='搬移工具',background='#53cf5d',font=('Arial',30,'bold')).pack()
frame1.pack(anchor='w')
frame2.pack(anchor='w')   
frame3.pack(anchor='center')   
frame4.pack(anchor='w')

root.mainloop()  # 放在主迴圈中

