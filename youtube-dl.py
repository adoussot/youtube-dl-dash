#!/usr/bin/python3.4
# coding: utf-8


import subprocess
import os
import sys
import getopt
import re 
import errno
from multiprocessing import Pool

def pretty_print(str):
    """
    :param arg1: replace unwanted character by _
    :type arg1: string
    """
    return '_'.join(str.split())

def gather_title(link):
    """
    :param arg1: url of the media to download with youtube-dl
    :type arg1: str
    """
    command =  "youtube-dl --get-filename -o '%(title)s' {}".format(link)
    title = subprocess.check_output(command.split(), shell=False)
    # convert Byte to String
    title = title.decode("utf-8")
    # remove the Quotes
    return pretty_print(title[1:-2])

def create_directory(title):
    """
    :param arg1: title of the output folder to create
    :type arg1: string
    """
    # create directory with the previous name
    path = "/home/mamadouhh/Documents/dev/dash/youtube/test/2/{}".format(title)
    mkdir_p(path)
    return path + "/"

def list_yt_medias(link):
    """
    :param arg1: url of the media to download with youtube-dl
    :type arg1: string
    """
    listVideo = "youtube-dl -F {}".format(link)
    output = subprocess.check_output(listVideo, shell=True)
    output = output.decode("utf-8")
    results = []
    for row in output.split("\n"):
        wordList = re.sub("[^\w]", " ", row).split()
        for i in range(len(wordList)):
            if (wordList[i] == "mp4"):
                results.append(wordList[i-1])
    return results

def process_file(command):
    """
    :param arg1: command to execute
    :type arg1: string
    """
    print("start execute command : {}".format(command))
    subprocess.check_output(command, shell=True)

def download_qualities(path, results, title, link):
    """
    :param arg1: url path where the output folder is
    :param arg2: differents file qualities
    :param arg3: media's title
    :param arg4: url of the media to download 
    :type arg1: string
    :type arg2: string[]
    :type arg3: string
    :type arg4: string
    """
    print("path :  {}".format(path))
    print("title :  {}".format(title))
    commands = []
    for result in results:
        commands.append(
            "youtube-dl -f {result} --output {path}{title}_{result}.'%(ext)s' {link}".format(result=result, path=path, title=title, link=link)
        )
    p = Pool(10)
    p.map(process_file, commands)
    p.close()
    p.join()
    # for i in commands:
    #     print("\ncommands: {}".format(i))


def mkdir_p(path):
    """
    :param arg1: url path where the output folder is
    :type arg1: string
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as err:
            if err.errno != 17:
                raise

def main(link):
    """
    :param arg1: url of the media to download with youtube-dl
    :type arg1: string
    """
    # fetch the youtube video's Name
    title = gather_title(link)
    print("title : {}".format(title))
    # create directory 
    path = create_directory(title)    
    #  list all the available video
    results = list_yt_medias(link)
    print("RESULT: ", results)
    # download files 
    download_qualities(path, results, title, link)

if __name__ =="__main__":   
    # import pdb; pdb.set_trace()
    print("Download every mp4 files of the youtube link: {}".format(sys.argv[1]))
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:y", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"

    main(sys.argv[1])



    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()
