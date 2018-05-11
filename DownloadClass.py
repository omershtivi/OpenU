import requests, os

def get_Movie():
    status_code = 200
    counter = 0
    
    while status_code == 200:
        response = requests.get('https://sslstream.bynetcdn.com/vod/mp4:vod/openu/PRV1/R46zT1CPEZ/App/R46zT1CPEZ_9.mp4/media_b400000_%d.ts' % counter)
        status_code = response.status_code
        if status_code == 200:
            filename = "media_b400000_%d.ts" % counter
            movie = open(filename, "w")
            movie.write(response.content)
            movie.close()
            counter = counter + 1
    return counter

def merge_Movies(number_of_parts):
    counter = 0
    cwd = os.getcwd()
    while counter < number_of_parts:
        os.system("cat media_b400000_%d.ts >> Lesson.ts" %counter)
        os.remove("%s/media_b400000_%d.ts" %(cwd, counter))
        counter = counter + 1

number_of_parts = get_Movie()
merge_Movies(number_of_parts)