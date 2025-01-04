import os
import tkinter as tk
from tkinter import ttk

def set_brightness(value):
    try:
        brightness_value = int(float(value))
        if brightness_value < 10:
            brightness_value = 10
        os.system(rf"WMIC /NAMESPACE:\\root\wmi PATH WmiMonitorBrightnessMethods WHERE 'Active=TRUE' CALL WmiSetBrightness Brightness={brightness_value} Timeout=0")
        brightness_label.config(text=f"当前亮度: {brightness_value}%")
    except Exception as e:
        brightness_label.config(text=f"错误: {e}")

def reset_brightness():
    brightness_slider.set(85)  # Reset slider to initial brightness
    set_brightness(85)  # Set brightness to initial brightness
    inp.delete(0, tk.END)

def get_initial_brightness():
    try:
        # Use WMIC to get the current brightness
        output = os.popen(r"WMIC /NAMESPACE:\\root\wmi PATH WmiMonitorBrightness GET CurrentBrightness").read()
        lines = output.splitlines()
        for line in lines:
            if line.strip().isdigit():
                return int(line.strip())
    except Exception as e:
        print(f"获取初始亮度失败: {e}")
    return 85  # Default to 85 if unable to get brightness



def read():
    inputed = inp.get()
    try:
        bright = int(inputed)
        set_brightness(bright)
        brightness_slider.set(bright)
    except:
        inp.delete(0, tk.END)
        inp.insert(0,"必须为整数")

# Create main window
root = tk.Tk()
root.title("没用的工具")
#root.geometry("800x600")
root.update_idletasks()
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"+{x_cordinate}+{y_cordinate}")  # Only set position, not size



# Get the initial brightness
current_brightness = get_initial_brightness()


# Brightness label
brightness_label = tk.Label(root, text=f"亮度: {current_brightness}%", font=("Arial", 14))
brightness_label.grid(row=0, column=0, columnspan=3, pady=10)

# Brightness slider
brightness_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=300, command=set_brightness)
brightness_slider.set(current_brightness)  # Set initial brightness to the current brightness
brightness_slider.grid(row=1, column=0, columnspan=3, pady=10)

# Entry field
inp = tk.Entry(root, font=("Arial", 14), width=10)
inp.grid(row=2, column=0, columnspan=3, pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, pady=10)

# Buttons
reset_button = tk.Button(button_frame, text="调至85%", command=reset_brightness, width=12)
reset_button.grid(row=0, column=0, padx=10)

second_button = tk.Button(button_frame, text="读取输入", command=read, width=12)
second_button.grid(row=0, column=1, padx=10)

exit_button = tk.Button(button_frame, text="退出", command=root.quit, width=12)
exit_button.grid(row=0, column=2, padx=10)

# Run the application
root.mainloop()
