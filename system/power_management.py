import os


flag = False

def set_shutdown_timer(minutes):
    global flag
    print(minutes, type(minutes))
    seconds = minutes * 60
    os.system(f'shutdown -s -t {seconds} -c " "')
    flag = True
    return True

def check_shutdown_status():
    global flag
    if flag:
        return True
    return False

def cancel_shutdown_timer():
    global flag
    os.system("shutdown /a")
    flag = False
    return True



