from __future__ import print_function
# Import standard modules
import wx
import os
from pprint import pprint
import re
import subprocess
import thread

# Import custom files
import VideoConvertGUI


class VideoConvertFrame(VideoConvertGUI.VCFrame):
    def __init__(self, parent):
        VideoConvertGUI.VCFrame.__init__(self, wx.GetApp().TopWindow)

        self.version = '0.1.0'
        self.SetTitle('VideoConvert ' + self.version)

        self.file_list = []
        self.ffmpeg_path = ''
        self.imagemagick_path = ''
        self.mediainfo_path = ''

    def event_button_start(self, event):
        print('event_button_start')
        self.execute_status = 'not_complete'
        thread.start_new_thread(execute,(self,None))
        while self.execute_status == 'not_complete':
            wx.YieldIfNeeded()

    def event_recursive(self, event):
        print('event_recursive')

    def event_reconvert(self, event):
        print('event_reconvert')

    def event_thumbnails(self, event):
        print('event_thumbnails')


def execute(self, fake=None):

    status = determine_paths(self)

    if status:

        self.file_list = []
        create_file_list(self, self.dir_picker.GetPath())
        print('\n\n\n====================================')
        pprint(self.file_list)

        get_media_info(self, self.file_list)
        print('\n\n\n====================================')
        pprint(self.file_list)

        get_number_frames(self, self.file_list)
        print('\n\n\n====================================')
        pprint(self.file_list)

        create_mp4(self, self.file_list)
        print('\n\n\n====================================')
        pprint(self.file_list)

        create_thumbnails(self, self.file_list)

    self.execute_status = 'complete'


def determine_paths(self):
    if os.path.isfile('paths.dat'):
        with open('paths.dat') as f:
            for line in f:
                chunks = line.split('=')
                if chunks[0].rstrip() == 'ffmpeg':
                    print('Found ffmpeg', chunks[1].rstrip())
                    self.ffmpeg_path = chunks[1].rstrip()
                elif chunks[0].rstrip() == 'mediainfo':
                    print('Found mediainfo:', chunks[1])
                    self.mediainfo_path = chunks[1].rstrip()
                elif chunks[0].rstrip() == 'imagemagick':
                    print('Found imagemagick:', chunks[1])
                    self.imagemagick_path = chunks[1].rstrip()
    else:
        msg = wx.MessageBox('Cannot find paths.dat file!')
        return False

    return True


def create_file_list(self, path):
    # print('create_file_list', path)
    self.textctrl_status0.SetValue('Building File List')
    wx.YieldIfNeeded()

    video_ext = ['.avi', '.mpg', '.mov', '.wmv']

    if self.check_recursive.IsChecked() == True:
        for root, sub_folders, files in os.walk(path):
            for f in files:
                if os.path.splitext(f)[1].lower() in video_ext:
                    self.file_list.append({'name': os.path.realpath(os.path.join(root, f))})

    elif self.check_recursive.IsChecked() == False:
        filenames = next(os.walk(path))[2]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in video_ext:
                self.file_list.append({'name': os.path.realpath(os.path.join(path, f))})

    # print('File list:')
    # pprint(file_list)

    self.textctrl_status0.SetValue('Building File List - Complete')
    wx.YieldIfNeeded()
    # return file_list


def get_media_info(self, file_list):
    self.textctrl_status0.SetValue('Determining Media Info')
    self.text_allfiles.SetLabel('0/' + str(len(file_list)))
    wx.YieldIfNeeded()

    file_count = 0

    for f in file_list:
        # print(f)
        # print('------------', os.path.split(f['name'])[0])
        self.textctrl_status1.SetValue(os.path.split(f['name'])[0])
        self.textctrl_status2.SetValue(os.path.split(f['name'])[1])
        wx.YieldIfNeeded()

        output = os.path.splitext(f['name'])[0] + '.mp4'

        if (self.check_reconvert.IsChecked() is False) and (os.path.isfile(output) is True):
            print('reconvert is unchecked')
            continue

        # media_info_path = r'C:\Portable_Software\mediainfo\MediaInfo.exe'
        media_info_path = self.mediainfo_path + '\\MediaInfo.exe'

        # media_info = os.popen('mediainfo ' + '"' + f['name'] + '"').readlines()
        media_info = os.popen(media_info_path + ' "' + f['name'] + '"').readlines()

        # print('\n\n===========================================================')
        # print(f)
        # for line in media_info:
        #     print(line.rstrip())
        # print('===========================================================')
        rotation_found = False
        duration_found = False
        duration = 0

        for line in media_info:
            try:
                if line.split(' ')[0] == 'Rotation':
                    rotation = line.split()[2][:-2]
                    f['rotation'] = rotation
                    rotation_found = True

                elif line.split(' ')[0] == 'Duration':
                    duration_line = line.split(': ')[1]
                    if not duration_found:
                        for chunk in duration_line.split(' '):
                            chunk2 = filter(None, re.split('(\d+)',chunk))
                            chunk2[1] = chunk2[1].rstrip('\r\n')
                            # print(chunk2)

                            if chunk2[1] == 'hr':
                                duration = duration + float(chunk2[0])*3600

                            elif chunk2[1] == 'mn':
                                duration = duration + float(chunk2[0])*60

                            elif chunk2[1] == 's':
                                duration = duration + float(chunk2[0])

                            elif chunk2[1] == 'ms':
                                duration = duration + float(chunk2[0])/1000

                        # print(duration)
                        f['duration'] = duration

                    duration_found = True

            except:
                pass

        # if not rotation_found:
        #     print('Rotation information not found!')
        # if not duration_found:
        #     print('Duration information not found!')

        file_count += 1
        self.text_allfiles.SetLabel(str(file_count) + '/' + str(len(file_list)))
        percentage = float(file_count) / float(len(file_list)) * 100
        # print(percentage)
        if percentage > 100:
                percentage = 100
        self.allfiles_progress_gauge.SetValue(percentage)
        wx.YieldIfNeeded()

    # print('file_list:')
    # pprint(file_list)

    self.textctrl_status0.SetValue('Determining Media Info - Complete')
    self.textctrl_status1.SetValue('')
    self.textctrl_status2.SetValue('')
    wx.YieldIfNeeded()


def get_number_frames(self, file_list):
    # print('get_number_frames')
    self.allfiles_progress_gauge.SetValue(0)
    self.text_allfiles.SetLabel('0/' + str(len(file_list)))
    self.textctrl_status0.SetValue('Determining Number of Frames')
    wx.YieldIfNeeded()

    # ffprobe_path = r'C:\Portable_Software\ffmpeg\bin\ffprobe.exe'
    ffprobe_path = self.ffmpeg_path + '\\ffprobe.exe'
    print(ffprobe_path)

    file_count = 1

    for f in file_list:
        # print(f)
        output = os.path.splitext(f['name'])[0] + '.mp4'

        if (self.check_reconvert.IsChecked() is False) and (os.path.isfile(output) is True):
            print('reconvert is unchecked')
            continue

        self.text_allfiles.SetLabel(str(file_count) + '/' + str(len(file_list)))
        percentage = float(file_count) / float(len(file_list)) * 100
        # print(value)
        if percentage > 100:
            percentage = 100
        self.allfiles_progress_gauge.SetValue(percentage)
        wx.YieldIfNeeded()

        self.textctrl_status1.SetValue(os.path.split(f['name'])[0])
        self.textctrl_status2.SetValue(os.path.split(f['name'])[1])
        wx.YieldIfNeeded()

        ffprobe_info = os.popen(ffprobe_path + ' -i "' + f['name'] + '" -show_frames').readlines()

        frames = 0

        for line in ffprobe_info:
            # print(line)
            if line == 'pict_type=P\n':
                frames += 1
                # print(frames)

        # print(frames)
        f['frames'] = frames

        file_count += 1


    self.textctrl_status0.SetValue('Determining Number of Frames - Complete')
    self.textctrl_status1.SetValue('')
    self.textctrl_status2.SetValue('')
    wx.YieldIfNeeded()



def create_mp4(self, file_list):
    print('create_mp4')
    self.allfiles_progress_gauge.SetValue(0)
    self.text_allfiles.SetLabel('0/' + str(len(file_list)))
    self.textctrl_status0.SetValue('Converting Videos')
    wx.YieldIfNeeded()

    ffmpeg_path = self.ffmpeg_path + '\\ffmpeg.exe'

    file_count = 1

    for f in file_list:
        # print(f)
        self.text_allfiles.SetLabel(str(file_count) + '/' + str(len(file_list)))
        value = float(file_count) / float(len(file_list)) * 100
        # print(value)
        self.allfiles_progress_gauge.SetValue(float(file_count) / float(len(file_list)) * 100)
        wx.YieldIfNeeded()

        self.textctrl_status1.SetValue(os.path.split(f['name'])[0])
        self.textctrl_status2.SetValue(os.path.split(f['name'])[1])
        wx.YieldIfNeeded()

        output = os.path.splitext(f['name'])[0] + '.mp4'
        print('output:', output)
        print(os.path.isfile(output))
        if self.check_reconvert.IsChecked() is False:
            if os.path.isfile(output) is True:
                print('reconvert is unchecked')
                continue

        elif self.check_reconvert.IsChecked() is True:
            print('reconvert is checked')

            if os.path.isfile(output):
                os.remove(output)       # delete file

        # print('output:', output)
        transpose = ''
        if 'rotation' in f:
            if f['rotation'] == '90':
                transpose = '-vf "transpose=1"'
                # transpose = '-vf rotate=(pi/2)'
            elif f['rotation'] == '180':
                transpose = '-vf hflip,vflip'
            elif f['rotation'] == '270':
                transpose = '-vf "transpose=2"'
                # transpose = '-vf rotate=(3*pi/2)'

        print('transpose:', transpose)

        # cmd = ffmpeg_path + ' -i "' + f['name'] + '" ' + transpose + ' -strict experimental "' + output + '"'
        cmd = ffmpeg_path + ' -i "' + f['name'] + '" ' + transpose + ' -strict experimental -metadata:s:v:0 rotate=0 "' + output + '"'

        print('cmd:', cmd)

        launch_converter(self, cmd, output, f['duration'], f['frames'])

        originaltime = os.path.getmtime(f['name'])
        os.utime(output, (originaltime, originaltime))

        file_count += 1

    self.textctrl_status0.SetValue('Converting Videos - Complete')
    self.textctrl_status1.SetValue('')
    self.textctrl_status2.SetValue('')
    self.allfiles_progress_gauge.SetValue(100)
    wx.YieldIfNeeded()


def launch_converter(self, cmd, filename, duration, frames):
    print('\n\nlaunch_converter')
    # print('cmd:', cmd)
    # print('filename:', filename)
    # print('duration:', duration)

    child = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    data = []

    while True:
        out = child.stderr.read(1)
        if out == '' and child.poll() != None:
            break

        # print(out)

        data.append(out)
        if out == '\r':
            # print(''.join(data))
            wx.YieldIfNeeded()

            line = ''.join(data)
            line2 = line.split()
            # print(line2)
            # print('line2[0]:', line2[0])
            try:
                if line2[0] == 'frame=':
                    framecount = line2[1]
                    # print(framecount)
                    percentage = float(framecount) / float(frames) * 100
                    # print(percentage)
                    if percentage > 100:
                        percentage = 100
                    self.current_progress_gauge.SetValue(percentage)
                    # self.text_filepercent.SetLabel(str(percentage) + '%')
                    self.text_filepercent.SetLabel('{0:.0f}%'.format(percentage))
                    wx.YieldIfNeeded()



            except:
                wx.YieldIfNeeded()
                pass

            data = []
            wx.YieldIfNeeded()
        wx.YieldIfNeeded()
    wx.YieldIfNeeded()


def create_thumbnails(self, file_list):
    print('create_thumbnails')
    self.allfiles_progress_gauge.SetValue(0)
    self.text_allfiles.SetLabel('0/' + str(len(file_list)))
    self.textctrl_status0.SetValue('Creating Thumbnails')
    wx.YieldIfNeeded()

    file_count = 1

    media_info_path = self.mediainfo_path + '\\MediaInfo.exe'
    imagemagick_path = self.imagemagick_path
    ffmpeg_path = self.ffmpeg_path + '\\ffmpeg.exe'

    for f in file_list:
        self.text_allfiles.SetLabel(str(file_count) + '/' + str(len(file_list)))
        percentage = float(file_count) / float(len(file_list)) * 100
        # print(value)
        if percentage > 100:
            percentage = 100
        self.allfiles_progress_gauge.SetValue(percentage)
        wx.YieldIfNeeded()

        self.textctrl_status1.SetValue(os.path.split(f['name'])[0])
        self.textctrl_status2.SetValue(os.path.split(f['name'])[1])
        wx.YieldIfNeeded()





        output = os.path.splitext(f['name'])[0] + '.jpg'
        print(output)
        converted_movie = os.path.splitext(f['name'])[0] + '.mp4'

        if self.check_thumbnails.IsChecked() is True:
            print('Recreate thumbnails is checked')

            if os.path.isfile(output):
                os.remove(output)       # Delete file

        elif (self.check_thumbnails.IsChecked() is False) and (os.path.isfile(output) is True):
            print('Recreate thumbnails is unchecked')
            continue

        media_info = os.popen(media_info_path + ' "' + f['name'] + '"').readlines()
        width = None
        height = None

        for line in media_info:
            try:
                if line.split(':')[0].rstrip() == 'Width':
                    width = line.split(':')[1]
                elif line.split(':')[0].rstrip() == 'Height':
                    height = line.split(':')[1]
            except:
                pass
        print('width:', width)
        print('height:', height)
        width = ''.join(width.split(' ')[1:-1])
        height = ''.join(height.split(' ')[1:-1])
        print('width:', width)
        print('height:', height)
        min_dimension = str(int(min(float(width), float(height))))
        print('min_dimension:', min_dimension)


        # ffmpeg_path = r'C:\Portable_Software\ffmpeg\bin\ffmpeg.exe'
        getphoto = ffmpeg_path + ' -ss 1 -i "' + converted_movie + '" -an -vframes 1 "' + output + '"'
        # getphoto = ffmpeg_path + ' -ss 1 -i "' + converted_movie + '" -i play.png -filter_complex "[1:v] scale=' + min_dimension + ':' + min_dimension + '[logo1]; [0:v][logo1] overlay=main_w/2-overlay_w/2:main_h/2-overlay_h/2" -vframes 1 "' + output + '"'

        # print('getphoto command:', getphoto)

        os.system(getphoto)

        # imagemagick_path = r'C:\Portable_Software\ImageMagick-6.9.0-0'

        im_command = imagemagick_path + '\convert.exe play.png -resize ' + min_dimension + 'x' + min_dimension + ' play_temp.png'
        os.system(im_command)

        im_command2 = imagemagick_path + '\composite.exe -gravity center play_temp.png "' + output + '" "' + output + '"'
        os.system(im_command2)

        os.remove('play_temp.png')

        originaltime = os.path.getmtime(f['name'])
        os.utime(output, (originaltime, originaltime))

        file_count += 1

    self.textctrl_status0.SetValue('Creating Thumbnails - Complete')
    self.textctrl_status1.SetValue('')
    self.textctrl_status2.SetValue('')
    self.allfiles_progress_gauge.SetValue(100)
    wx.YieldIfNeeded()



















if __name__ == '__main__':
    app = wx.App(False)
    frame = VideoConvertFrame(None)
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()