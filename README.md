# OpenU

Script located in `DownloadClass.py` allowes downloading and combining TS files to a complete Lesson.

Uses following modules : 
* `requests` - Used for the HTTP requests to get playlist and download the clip
* `sys` - Used for reading input arguments and exiting gracefully
* `webbrowser` - Used for triggering browser open
* `re` - Used for regex search
* `time` - used for creating delay
* `browser_cookie3` - Used for getting Cookies
* `socket` - Used for reachability tests

```
#################################################################################
#       None interactive mode useage:                                           #
#       DownloadClass.py <Course ID> <Group ID> <Semester> <Lesson Number>      #
#       Example:         DownloadClass.py 12345 123_01 18b 1                    #
#################################################################################
Please choose operation mode
1: Use playlist url to fetch specific lesson
2: Use chunk URL to fetch specific lesson
3: Provide Course ID and Group ID for interactive menu
4: Will fetch all your courses and groups
>
```
