import getopt
import sys
import os
import subprocess

def help():
    help_message = """ 
Youtubedl-Dash : A short python script for downloading every mp4 youtube files from a specific link

Usage: python3 youtubedl-dash.py [arguments] 

Arguments: 
  -h or --help  : Show help (this message) and exit
  -l or --link  : The video to download link   
  -d or --dir   : the output directory
"""
    print(help_message)
    

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:v", ["help", "link=", "output_dir="])
    except getopt.GetoptError as err:
        print(err) 
        help()
        sys.exit(2)

    output_dir = None
    link = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-l", "--link"):
            print("linkarg: {}".format(arg))
            link = arg
        elif opt in ("-d", "--dir"):
            output_dir = arg

        else:
            assert False, "unhandled option"
    
    if (link is not None):
        print("link: {}".format(link))
        subprocess.call(["python3", "youtubedl-dash.py", link])

if __name__ == "__main__":
    main()