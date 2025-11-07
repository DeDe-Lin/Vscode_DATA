import tkinter as tk
import shutil,traceback
from tkinter import messagebox # <-- 1. 導入 messagebox
selection_vars = {}

root = tk.Tk()   # 建立 tkinter 視窗物件
root.title('版更協助搬檔工具')        # 設定標題
# width = 800
# height = 400
# left = 0
# top = 0
# root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置
root.configure(background='#53cf5d')  

testtex = tk.StringVar()
input1 = tk.StringVar(value='\\\\192.168.6.81\e$\版本更新\  #記得版更日期')
input2 = tk.StringVar(value='\\\\192.168.6.81\d$\PROJECT')
input3 = tk.StringVar(value='\\\\192.168.6.82\d$\PROJECT')
input4 = tk.StringVar(value='\\\\192.168.6.83\d$\PROJECT')

testtex.set("錯誤訊息顯示區")


def check_before_copy():
    # 彈出確認視窗
    # askyesno() 函數：詢問使用者「是否」執行，並返回 True 或 False
    confirm = messagebox.askyesno(
        title="執行確認",
        message="確定要開始檔案複製操作嗎？\n請確認路徑設定無誤！"
    )

    # 3. 條件判斷
    if confirm:
        # 如果使用者點擊「是 (Yes)」，則執行原本的函式
        copy_with_ignore_simple()
    else:
        # 如果使用者點擊「否 (No)」，則取消操作
        testtex.set("操作已取消。")
def function_choose():
    import traceback, os
    f1 = input1.get().strip()
    if not f1:
        testtex.set("請填入來源路徑")
        return
    try:
        # 清除 inner_frame 內先前的 widget 與選項變數
        for w in inner_frame.winfo_children():
            w.destroy()
        selection_vars.clear()

        # 填入 Checkbutton（放到 inner_frame）
        entries = sorted(os.listdir(f1))
        if not entries:
            tk.Label(inner_frame, text="資料夾為空", bg=inner_frame.cget('bg')).pack(anchor='w')
        else:
            tk.Label(inner_frame, text="請勾選要忽略的項目：", bg=inner_frame.cget('bg')).pack(anchor='w')
            for e in entries:
                var = tk.BooleanVar(value=False)
                cb = tk.Checkbutton(inner_frame, text=e, variable=var, anchor='w', bg=inner_frame.cget('bg'))
                cb.pack(fill='x', anchor='w')
                selection_vars[e] = var

        # 更新 scrollregion
        canvas_choose.configure(scrollregion=canvas_choose.bbox('all'))

        testtex.set(f"已查詢：{f1} （共 {len(entries)} 項）")
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        testtex.set(f"錯誤：{e}")
        
def copy_with_ignore_simple():
    import shutil
    from pathlib import Path
    import traceback

    src_path = input1.get().strip()
    targets = [input2.get().strip(), input3.get().strip(), input4.get().strip()]
    targets = [t for t in targets if t]  # 保留非空目標

    if not src_path or not targets:
        testtex.set("請填入來源與至少一個目標路徑")
        return

    src = Path(src_path)
    if not src.exists():
        testtex.set(f"來源不存在：{src}")
        return
    if not src.is_dir():
        testtex.set("來源不是資料夾，請填入資料夾路徑")
        return

    # 取得要忽略的項目（只取 basename）
    ignore_list = [name for name, var in selection_vars.items() if var.get()]
    patterns = [Path(n).name for n in ignore_list]
    ignore_fn = shutil.ignore_patterns(*patterns) if patterns else None

    results = []
    for t in targets:
        try:
            dst = Path(t)
            # 基本安全檢查：避免目標與來源相同或目標位於來源內造成遞迴
            if dst.resolve() == src.resolve():
                results.append(f"跳過（相同路徑）：{dst}")
                continue
            if src.resolve() in dst.resolve().parents:
                results.append(f"跳過（目標位於來源內，會造成遞迴）：{dst}")
                continue

            # 建立目標資料夾（copytree with dirs_exist_ok 會合併）
            dst.mkdir(parents=True, exist_ok=True)

            if ignore_fn:
                shutil.copytree(src, dst, ignore=ignore_fn, copy_function=shutil.copy2, dirs_exist_ok=True)
            else:
                shutil.copytree(src, dst, copy_function=shutil.copy2, dirs_exist_ok=True)

            results.append(f"完成：{dst}")
        except Exception as e:
            tb = traceback.format_exc()
            results.append(f"失敗：{t} → {e}")

    # 顯示結果（每行一個目標的狀態）
    testtex.set("\n".join(results))

frame1 = tk.Frame(root, pady=10, padx=10, bg='#c90')   # 第一個 Frame 元件
frame_choose = tk.LabelFrame(root, pady=10, padx=10, bg='#c09')   # 第一個 Frame 元件
canvas_choose = tk.Canvas(frame_choose, bg=frame_choose.cget('bg'), highlightthickness=0, width=760, height=200)
vscroll = tk.Scrollbar(frame_choose, orient='vertical', command=canvas_choose.yview)
canvas_choose.configure(yscrollcommand=vscroll.set)
inner_frame = tk.Frame(canvas_choose, bg=frame_choose.cget('bg'))
canvas_choose.create_window((0,0), window=inner_frame, anchor='nw')

def _on_frame_configure(event):
    canvas_choose.configure(scrollregion=canvas_choose.bbox('all'))
inner_frame.bind('<Configure>', _on_frame_configure)

# 支援滑鼠滾輪（Windows）
def _on_mousewheel(event):
    canvas_choose.yview_scroll(int(-1*(event.delta/120)), "units")
canvas_choose.bind_all("<MouseWheel>", _on_mousewheel)

canvas_choose.pack(side='left', fill='both', expand=True)
vscroll.pack(side='right', fill='y')



frame2 = tk.Frame(root, pady=10, padx=10, bg='#09c')   # 第二個 Frame 元件
frame3 = tk.Frame(root, pady=10, padx=10, bg='#9c0')   # 第三個 Frame 元件
frame4 = tk.Frame(root, pady=10, padx=10, bg='#0c9')   # 第四個 Frame 元件


tk.Label(frame1,text='請輸入移動前位置：').pack(side='left')
tk.Entry(frame1,textvariable=input1,width=50,borderwidth=5).pack(side='left',padx=10)
tk.Button(frame1, text='查詢',font=('微軟正黑體',20,'bold'),width=4,height=1,activeforeground='#f00',command=function_choose).pack(side='left',padx=20)


tk.Label(frame2,text='請輸入移動後位置：').pack(side='left')
tk.Entry(frame2,textvariable=input2,width=50,borderwidth=5).pack(side='top',padx=10)
tk.Entry(frame2,textvariable=input3,width=50,borderwidth=5).pack(side='top',padx=10)
tk.Entry(frame2,textvariable=input4,width=50,borderwidth=5).pack(side='top',padx=10)
tk.Button(frame3, text='複製',font=('微軟正黑體',20,'bold'),width=4,height=1,activeforeground='#f00',command=check_before_copy).pack(side='left',padx=20)
#tk.Button(frame3, text='搬移',font=('微軟正黑體',20,'bold'),width=4,height=1,activeforeground='#f00',command='').pack(side='left',padx=20)
tk.Label(frame4,textvariable=testtex).pack(side='left')


tk.Label(root, text='版更協助搬檔工具',background='#53cf5d',font=('Arial',30,'bold')).pack()
frame1.pack(anchor='w')
frame_choose.pack(anchor='w')
frame2.pack(anchor='w')   
frame3.pack(anchor='center')   
frame4.pack(anchor='w')
root.mainloop()  # 放在主迴圈中

