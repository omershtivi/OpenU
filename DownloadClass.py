import requests, os, sys

def get_Movie():
    status_code = 200
    filename = "Lesson.ts"
    counter = 0

    while status_code == 200:
        response = requests.get('%s_%d.ts' % (sys.argv[1], counter))
        status_code = response.status_code
        if status_code == 200:
            movie = open(filename, "ab")
            movie.write(response.content)
            movie.close()
            counter = counter + 1
    return counter

number_of_parts = get_Movie()

