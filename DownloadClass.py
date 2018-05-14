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
        perc=c/llen
        perc=perc*100.0
        print ('%f percent done!' % perc)
    #end of for
#end of downloadClips

crs = input("Please provide course code...\r\n>")
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
cem=str(year)+cem
grp = input("Please Provide group code, use underscore for delimiter\r\n>")
amount = get_MovieAmount(crs, cem, grp)
print("found %d Lessons " % amount)
dec = input("Please select witch Lesson you want\r\nUse 0 for all")
if dec=='all':
    print("Under Construction")
elif int(dec)>amount:
    print(dec)
    print(amount)
    print("you've chosen a wrong Lesson!")
else:
    downloadClips(getClipUrl(crs, cem, grp, int(dec)), "lesson.ts")
