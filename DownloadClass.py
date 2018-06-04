import requests, os, sys, webbrowser, re, time, browser_cookie3, socket

def getClipUrl(crs, cem, grp, n):
    response = requests.get('https://api.bynetcdn.com/Redirector/openu/manifest/c%s_%s_%s_%d_HD_mp4/HLS/playlist.m3u8' % (crs, cem, grp,n))
    if response.status_code!=200:
        print("Failed to get 200 from server! got %d instead" % response.status_code)
        sys.exit(1)

    urlStr=response.text.index('https')
    urlEnd=response.text.index('m3u8')+4
    return response.text[urlStr:urlEnd]
#end of getClipUrl

def get_MovieAmount(crs, cem, grp):
    status_code = 200
    counter = 1
    while status_code == 200:
        response=requests.get(getClipUrl(crs, cem, grp, counter))
        if response.status_code!=200:
            print("Failed to get 200 from server! got %d instead" % response.status_code)
            sys.exit(1)

        llen=len(response.text.splitlines())
        if llen<40:
            return counter-1
        counter=counter+1
    #end of while
#end of get_MovieAmount

def downloadClips(s, filename):
    response=requests.get(s)
    if response.status_code!=200:
        print("Failed to get 200 from server! got %d instead" % response.status_code)
        sys.exit(1)

    llen=len(response.text.splitlines())
    c=0
    for line in response.text.splitlines():
        c=c+1
        if not line.startswith('#'):
            response=requests.get(s[0:s.index('chunklist')]+line)
            if response.status_code!=200:
                print("Failed to get 200 from server! got %d instead" % response.status_code)
                sys.exit(1)

            status_code = response.status_code
            if status_code == 200:
                movie = open(filename, "ab")
                movie.write(response.content)
                movie.close()
            #end of internal if
        # end of if
        if c%15==0:
            # print progress 
            perc=c/llen
            perc=perc*100.0
            print ('%d percent done!' % perc)
        #end of if
    #end of for
#end of downloadClips

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

def find_info():
    webbrowser.open("https://sheilta.apps.openu.ac.il/pls/dmyopt2/sheilta.myop")

    time.sleep(30)

    jar = requests.cookies.RequestsCookieJar()
    cj = browser_cookie3.load(domain_name='openu.ac.il')
    #print(cj)
    for cookie in cj:
        if 'openu.ac.il' in cookie.domain :
            jar.set(cookie.name, cookie.value, domain=cookie.domain, path='/')
    #print(jar)
    response=requests.get("https://sheilta.apps.openu.ac.il/pls/dmyopt2/course_info.courses", cookies=jar)
    if response.status_code!=200:
        print("Failed to get 200 from server! got %d instead" % response.status_code)
        sys.exit(1)

    #print(response.text)
    
    for loc1 in re.findall('https\:\/\/.+course.php\?.+?\"',response.text):
        course=loc1.split("course=")[1].split("&semester")[0]
        tmp=response.text.find("course_info.courseinfo?p_kurs="+course[1:])
        grp=response.text[tmp:tmp+100].split("p_MERKAZ_LIMUD=")[1].split("&")[0]+"_"+response.text[tmp:tmp+100].split("p_KVUTZAT_LIMUD=")[1].split("&")[0]
        semester=response.text[tmp:tmp+100].split("p_semester=20")[1].split("&")[0]
        print("Course="+course+", Group="+grp + ", Semester=" + semester)
# end of find_info

def reachability(hostname):
    try:
        socket.gethostbyname(hostname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((hostname,80))
        if result == 0:
            return 1
        else:
            return 0
    except socket.error:
        return 0
# end of resolve

print("#################################################################################")
print("#\tNone interactive mode useage:\t\t\t\t\t\t#\r\n#\t%s <Course ID> <Group ID> <Semester> <Lesson Number>\t\t#\r\n#\tExample:\t %s 30111 780_01 18b 1\t\t\t#" % (sys.argv[0], sys.argv[0]))
print("#################################################################################")
if len(sys.argv)>1:
    print(sys.argv[1], sys.argv[3], sys.argv[2], int(sys.argv[4]))
    downloadClips(getClipUrl(sys.argv[1], sys.argv[3], sys.argv[2], int(sys.argv[4])), "lesson_"+sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[4]+".ts")
    sys.exit(0)
if not reachability('sheilta.apps.openu.ac.il'):
    print("Sorry, there is a connectivity problem o_O please correct it first")
    sys.exit(2)

opType=str(input("Please choose operation mode\r\n1: Use playlist url to fetch specific lesson\r\n2: Use chunk URL to fetch specific lesson\r\n3: Provide Course ID and Group ID for interactive menu\r\n4: Will fetch all your courses and groups\r\n>"))
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
    crs=grp=cem=""
    while crs == "" :
        crs = input("Please provide course code...\r\n>")
    while grp=='':
        grp = input("Please Provide group code, use underscore for delimiter\r\n>")
    while cem=='':
        cem = input("Please Provide desired semester\r\n>")
    amount = get_MovieAmount(crs, cem, grp)
    print("found %d Lessons\r\n" % amount)

    flag=0
    while not flag:
        flag=menu(amount, crs, cem, grp)
    # end of while
elif opType=='4':
    find_info()
#end of elseif

