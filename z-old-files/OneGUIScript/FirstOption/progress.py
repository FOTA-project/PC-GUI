from tkinter import * 
from tkinter import ttk
import sys, time, os ,ctypes



def ShowProgressBar():

    INSTRUCTION_WRITE_MAX_REQUESTS    = -4
    INSTRUCTION_COMM_TIMEOUT          = -2
    INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

      
    # creating tkinter window 
    root = Tk() 
    root.geometry("300x100+50+250")
    root.title(" Flashing progress ....")
    
    root.progress_bar = ttk.Progressbar(root, orient = 'horizontal', length = 286, mode = 'determinate')
    root.progress_bar.pack(pady  =35)



    global f     
    f = open('progress.txt', 'r')
    f.seek(0)

    progress = 0
    maxRequests = -1

    while progress != maxRequests:
        progress = f.readline().strip()
        f.flush()
        
        if progress == '':
            time.sleep(0.000001 * 500) # 500us
            continue
            
        elif int(progress[:2], 10) == INSTRUCTION_WRITE_MAX_REQUESTS:
            maxRequests = int(progress.split()[1])
            print("progress.py: maxRequests = %d\n" %(maxRequests))
            
        elif int(progress[:2], 10) == INSTRUCTION_COMM_TIMEOUT:
            # TODO handle this
            root.progress_bar.stop()
            sys.exit(1)
            print("Widget.close() ------ 1\n")

        elif int(progress[:2], 10) == INSTRUCTION_TERMINATE_ON_SUCCESS:
            root.progress_bar.stop()
            ctypes.windll.user32.MessageBoxW(0, "Done!", "Flashing", 0) 
            sys.exit(1)
            print("Widget.close() ------ 2\n")
            #f.close()
            
        else: # normal number
      
            root.progress_bar["maximum"] = str(maxRequests)
            root.progress_bar["value"] = str(progress)
            root.progress_bar.update()
        
            print("progress.py: progress = %d\n" %(int(progress)))
            time.sleep(0.000001 * 500) # 500us
          
          
          

