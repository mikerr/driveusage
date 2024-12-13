import time,os,subprocess
import pygame

screen = pygame.display.set_mode()
pygame.mouse.set_visible(False)
pygame.display.flip()
pygame.font.init()
font = pygame.font.SysFont(None, 24)

def checkend(i):
    factor = 1
    if i.endswith('M'): factor = 1
    if i.endswith('G'): factor = 1024
    if i.endswith('T'): factor = 1024 * 1024
    i = i[:-1] # remove last letter
    i = float(i) * factor
    return i

def printtext(text,x,y):
    img = font.render(text, True, pen)
    screen.blit(img, (x, y))

while True:
    output = subprocess.check_output("lsblk",text=True)
    lines = output.split("\n")

    # find largest partition
    parts = []
    for line in lines:
        info = line.split()
        if len(info) == 0: break
        name = info[0][2:] # ignore symbol at start
        type = info[5]
        if type == 'part' and name[:2] == 'sd':
            size = checkend(info[3])
            parts.append((size,name))
    if (len(parts) <1) : 
        screen.fill((0,0,0))
        pygame.display.flip()
        continue
    largestpart = sorted(parts)[-1][1]
    time.sleep(1)

    try:
        output = subprocess.check_output(["df","-h","/dev/" + largestpart],text=True)
    except: continue
    if (largestpart not in output) :
        if not os.path.exists("/tmp/hdd"):
            os.mkdir("/tmp/hdd")
        try:
            output = subprocess.check_output(["sudo","mount","/dev/" + largestpart, "/tmp/hdd"],text=True)
            output = subprocess.check_output(["df","-h","/dev/" + largestpart],text=True)
        except: continue
    lines = output.split("\n")

    info = lines[-2].split()
    name = info[0]
    size = info[1]
    usage = info[2]
    avail = info[3]
    mount = info[5]

    size2 =  checkend(size)
    usage2 = checkend(usage)

    y = 0
    pen = (0,255,255)
    printtext("USB DRIVE USAGE")
    
    y += 50
    pen = (0,255,255)
    text = "%s       %s / %s " % (name,usage, size)
    printtext(text,0,y)
    
    # draw gauge
    y += 30
    plength =  int(240 * (usage2 / size2))
    pygame.draw.rect(screen,pen,(0,y,240,20),2)
    pygame.draw.rect(screen,pen,(0,y,plength,20))
    
    # show files
    y += 55
    printtext("Files",0,y)
    
    y += 20
    dir_list = os.listdir("/")
    for name in dir_list:
        printtext(name,20,y)
        y += 20
        if y > 240 : break
    
    output = subprocess.check_output(["sudo","umount","/dev/" + largestpart],text=True)
    pygame.display.flip()
    time.sleep(5)
