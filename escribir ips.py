import pyautogui, time, pyperclip

time.sleep(10)

for a in range(0, 255, 10):
    pyperclip.copy(f"http://172.16.11.{a}/ \n")
    pyautogui.hotkey('ctrl', 'v')
    for b in range(1, 10):
        pyperclip.copy(f"http://172.16.11.{a+b}/ \n")
        pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy("\n")
    pyautogui.hotkey('ctrl', 'v')

#for ip in range(1, 255):
#    pyperclip.copy(f"http://172.16.9.{ip}/ \n")
#    pyautogui.hotkey('ctrl', 'v')
