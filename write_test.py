import sys,time

progress=0
while progress < 110:
    f=open('progress.txt', 'w')
    f.write(str(progress))
    f.close()
    time.sleep(0.5)
    progress+=10