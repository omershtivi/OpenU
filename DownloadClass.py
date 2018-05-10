import requests, os

def get_Movie():
    status_code = 200
    counter = 0
	
    while status_code == 200:
        response = requests.get('https://sslstream.bynetcdn.com/vod/mp4:vod/openu/PRV1/R46zT1CPEZ/App/R46zT1CPEZ_9.mp4/media_b400000_%d.ts' % counter)
        filename = "./tmp/media_b400000_%d.ts" % counter
        movie = open(filename, "w")
        movie.write(response.content)
        movie.close()
        counter = counter + 1
        status_code = response.status_code


def merge_Movies():
    os.system("cat ./tmp/*.ts > Lesson.ts")

get_Movie()
merge_Movies()

