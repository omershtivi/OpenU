import requests, os, sys, datetime

def getClipUrl(crs, cem, grp, n):
    response = requests.get('https://api.bynetcdn.com/Redirector/openu/manifest/c%s_%s_%s_%d_HD_mp4/HLS/playlist.m3u8' % (crs, cem, grp,n))
    status_code = response.status_code

    urlStr=response.text.index('https')
    urlEnd=response.text.index('m3u8')+4
    return response.text[urlStr:urlEnd]
#end of getClipUrl

def get_MovieAmount(crs, cem, grp):
    status_code = 200
    counter = 1
    while status_code == 200:
        url=getClipUrl(crs, cem, grp, counter)
        response2=requests.get(url)
        llen=len(response2.text.splitlines())
        if llen<40:
            return counter-1
        counter=counter+1

    #end of while
#end of get_MovieAmount

def downloadClips(s, filename):
    response=requests.get(s)
    llen=len(response.text.splitlines())
    c=0
    for line in response.text.splitlines():
        c=c+1
        if not line.startswith('#'):
            response=requests.get(s[0:s.index('chunklist')]+line)
            status_code = response.status_code
            if status_code == 200:
                movie = open(filename, "ab")
                movie.write(response.content)
                movie.close()
            #end of internal if
        # end of if
        if c%15==0:
            #will print progress every chunk
            perc=c/llen
            perc=perc*100.0
            print ('%d percent done!' % perc)
        #end of if
    #end of for
#end of downloadClips

def findCem():
    year = (datetime.datetime.now().year-2000)
    m= datetime.datetime.now().month
    if m==1:
        cem="a"
    elif m<=6:
        cem="b"
    elif m<=9:
        cem="c"
    else:
        cem="a"
    return str(year)+cem
#end of findCem

def menu(amount, crs, cem, grp):
    dec = input("Please select witch Lesson you want\r\nUse 0 for all Or \"-1\" to exit\r\n")
    if dec== '-1':
        print ("Thank you for using %s !\r\nGood Day" % sys.argv[0])
        return 1
    elif dec == '0':
        for x in range(1, amount+1):
            downloadClips(getClipUrl(crs, cem, grp, x), "lesson_"+str(x)+".ts")
        # end of for
        return 1
    elif int(dec)>amount:
        print("you've chosen a wrong Lesson!")
    else:
        downloadClips(getClipUrl(crs, cem, grp, int(dec)), "lesson_"+dec+".ts")
# end of menu

print("None interactive mode useage:\t%s <Course ID> <Group ID> <Lesson Number>\r\nExample:\t %s 30111 780_01 1" % (sys.argv[0], sys.argv[0]))
if len(sys.argv)>1:
    downloadClips(getClipUrl(sys.argv[1], findCem(), sys.argv[2], int(sys.argv[3])), "lesson_"+sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[3]+".ts")
opType=input("Please choose operation mode\r\n1: Use playlist url to fetch specific lesson\r\n2: Use chunk URL to fetch specific lesson\r\n3: Provide Course ID and Group ID for interactive menu\r\n>")
if opType=='1':
    s=input("Please provide url to M3U playlist file\r\n>")
    downloadClips(s, 'lesson.ts')
elif opType=='2':
    s=input("Please provide url to a clip, omit clip number and \".ts\"\r\n> ")
    status_code = 200
    counter = 0
    while status_code == 200:
        response = requests.get('%s_%d.ts' % (s,counter))
        status_code = response.status_code
        if status_code == 200:
            movie = open('lesson.ts', "ab")
            movie.write(response.content)
            movie.close()
            counter = counter + 1
elif opType=='3':
    crs=grp=""
    while crs == "" :
        crs = input("Please provide course code...\r\n>")
    while grp=='':
        grp = input("Please Provide group code, use underscore for delimiter\r\n>")
    cem = findCem()
    amount = get_MovieAmount(crs, cem, grp)
    print("found %d Lessons\r\n" % amount)

    flag=0
    while not flag:
        flag=menu(amount, crs, cem, grp)
    # end of while
#end of else

