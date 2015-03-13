import subprocess
import sys
import os
import re

def execute(cmd,filename,duration):
    #print cmd
    #print duration
    child = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    complete = False
    data = []
    while True:
        out = child.stderr.read(1)
        if out == '' and child.poll() != None:
            break
        if out != '':
##            sys.stdout.write(out)
##            sys.stdout.flush()
            if out != '\r':
                data.append(out)
            else:
                line = ''.join(data)
                line2 = line.split()
                for chunk2 in line2:
                    if chunk2[0:4] == 'time':
                        #print chunk2
                        chunk3 = re.split('[=:.]',chunk2)
                        #print chunk3
                        try:
                            current_duration = float(chunk3[1])*3600 + float(chunk3[2])*60 + float(chunk3[3]) + float(chunk3[4])/100

                            #print current_duration
                            percent = float(current_duration/duration*100)
                            print filename + '.mp4 - Percent complete:', str(percent) + '%'
                        except: pass
                data = []
                #data.append(out)

ffmpeg_path = 'D:\\Portable_Software\\ffmpeg\\bin\\ffmpeg.exe'
mediainfo = 'D:\\Portable_Software\\mediainfo\\mediainfo.exe'

#path = 'C:\\Users\\bilyejd\\Desktop\\test'
path = os.getcwd()
#print 'path;', path


filelist = []
videoext = ['.avi','.mpg','.mov','.wmv','.MOV','.AVI','.MPG','.WMV']

for root, subfolders, files in os.walk(path):
    for file in files:

        #print file
        #print os.path.basename(file)
        for extension in videoext:

            if os.path.splitext(file)[1] == extension:
                print '============================================================'
                #print 'root:',root
                #print 'subfolders:',subfolders
                #print 'file:',file
                basename = os.path.splitext(file)[0]
                ext = os.path.splitext(file)[1]
                fullpath = os.path.abspath(file)
                fullpath = root + '\\' + file
                print 'fullpath:', fullpath
                #print basename
                #print ext[1:]

                #print 'run command on:', file
                output2 = root + '\\' + basename + '_modified.mp4'
                output = root + '\\' + basename + '.mp4'
                outputpic = root + '\\' + basename + '.jpg'
                #print output

                movie_time = os.path.getmtime(fullpath)
                getinfo = '"' + mediainfo + '" "' + fullpath + '"'

                test = subprocess.Popen(getinfo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                video_info = test.stdout.read().split('\n')

                rotation_found = 0
                duration_found = 0
                tp = ''
                duration = 0
                for line in video_info:
                    if line.split(' ')[0] == 'Rotation':
                        rotation_found = 1
                        rotation_deg = line.split(': ')[1][:-3]
                        print rotation_deg
                        if rotation_deg == '90':
                            tp = '-vf "transpose=1" '
                        elif rotation_deg == '180':
                            tp = '-vf "hflip,vflip" '
                        else:
                            tp = ''
                        #print 'tp:',tp
                    if line.split(' ')[0] == 'Duration':
                        if duration_found == 0:

                            duration_line = line.split(': ')[1]
                            for chunk in duration_line.split(' '):
                                chunk2 = filter(None, re.split('(\d+)',chunk))
                                chunk2[1] = chunk2[1].rstrip('\r\n')
                                #print chunk2

                                if chunk2[1] == 'mn':
                                    #print 'found mn'
                                    duration = duration + float(chunk2[0])*60
                                    #print duration
                                if chunk2[1] == 's':
                                    #print 'found s'
                                    duration = duration + float(chunk2[0])
                                    #print duration

                            duration_found = 1
                            #print 'Duration:', duration
                if rotation_found == 0:
                    print 'Rotation information not found!'

                if os.path.isfile(output) == False:
                    cmd = ffmpeg_path + ' -i "' + fullpath + '" -sameq '+ tp + '"' + output + '"' # Rotate 90
                    #print cmd
                    execute(cmd,basename,duration)
                    os.utime(output,(movie_time,movie_time)) #set the converted movie date to the same as the original video

                else:
                    print 'mp4 file has already been created!'

                if os.path.isfile(outputpic) == False:
                    getphoto = ffmpeg_path + ' -ss 1 -i "' + output + '" -an -vframes 1 "' + outputpic + '"'
                    os.system(getphoto)
                    os.utime(outputpic,(movie_time,movie_time))
                else:
                    print 'Video thumbnail has already been created!'