import sys
from PySide import QtGui, QtCore
import time
import os
import re
import subprocess
from pprint import pprint
import pexpect
import video_convert_gui


class MainWindow(QtGui.QMainWindow, video_convert_gui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.assign_widgets()

        # Set up variables
        self.version = '0.3.0'
        self.setWindowTitle('VideoConvert ' + self.version)
        self.setWindowIcon(QtGui.QIcon('movie.png'))

        self.file_list = []
        self.file_list_reconvert = []
        self.file_list_thumbnails = []
        self.ffmpeg_path = ''
        self.ffprobe_path = ''
        self.imagemagick_path = ''
        self.mediainfo_path = ''

        self.convert_path = ''
        self.composite_path = ''

    def assign_widgets(self):
        self.pushButton_Browse.clicked.connect(self.browse_pushed)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok_pushed)
        self.buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(QtCore.QCoreApplication.instance().quit)

    def browse_pushed(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Select a folder to convert videos")

        if directory:
            self.lineEdit_FolderPath.setText(directory)

    def ok_pushed(self):
        print('OK Pushed')
        status = self.determine_paths()

        recursiveBool = self.checkBox_Recursive.checkState()
        reconvertBool = self.checkBox_Reconvert.checkState()
        thumbnailsBool = self.checkBox_Thumbnails.checkState()

        if status:
            self.create_file_list(self.lineEdit_FolderPath.text(), recursiveBool, reconvertBool, thumbnailsBool)

    ##################
    # Worker functions
    ###################

    def set_status(self, status):
        self.lineEdit_Status.setText(status)

    def set_folder(self, folder):
        self.lineEdit_Folder.setText(folder)

    def set_file(self, file):
        self.lineEdit_File.setText(file)

    def set_CurrentPercent(self, percent):
        if percent == 0:
            self.label_CurrentPercent.setText('---')
        else:
            self.label_CurrentPercent.setText('{:.1%}'.format(percent))


        self.progressBar_Current.setValue(percent*100)

    def set_AllPercent(self, percent):
        self.progressBar_All.setValue(percent*100)

    def set_AllFraction(self, s):
        self.label_AllFraction.setText(s)

    def determine_paths(self):
        if os.name == 'posix':
            try:
                subprocess.call(['which', 'mediainfo'])
                self.mediainfo_path = 'mediainfo'
            except:
                print('mediainfo not found!')

                msgBox = QtGui.QMessageBox()
                msgBox.setText('mediainfo not found!')
                msgBox.exec_()
                return False

            try:
                subprocess.call(['which', 'convert'])
                self.convert_path = 'convert'
            except:
                print('convert not found!')

                msgBox = QtGui.QMessageBox()
                msgBox.setText('convert not found!')
                msgBox.exec_()
                return False

            try:
                subprocess.call(['which', 'composite'])
                self.composite_path = 'composite'
            except:
                print('composite not found!')

                msgBox = QtGui.QMessageBox()
                msgBox.setText('composite not found!')
                msgBox.exec_()
                return False

            try:
                subprocess.call(['which', 'ffmpeg'])
                self.ffmpeg_path = 'ffmpeg'

            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText('ffmpeg not found!')
                msgBox.exec_()
                return False

            try:
                subprocess.call(['which', 'ffprobe'])
                self.ffprobe_path = 'ffprobe'

            except:
                msgBox = QtGui.QMessageBox()
                msgBox.setText('ffprobe not found!')
                msgBox.exec_()
                return False

            return True

        else:
            if os.path.isfile('paths.dat'):
                with open('paths.dat') as f:
                    for line in f:
                        chunks = line.split('=')
                        if chunks[0].rstrip() == 'ffmpeg':
                            self.ffmpeg_path = chunks[1].rstrip()
                        elif chunks[0].rstrip() == 'mediainfo':
                            self.mediainfo_path = chunks[1].rstrip()
                        elif chunks[0].rstrip() == 'imagemagick':
                            self.imagemagick_path = chunks[1].rstrip()
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText('Cannot find the paths.dat file!')
                msgBox.exec_()

    # Start create file list functions

    def create_file_list(self, directory, recursiveBool, reconvertBool, thumbnailsBool):
        print('create_file_list_start')
        self.set_status('Step 1: Creating File List')
        self.progressBar_Current.setRange(0, 0)
        self.label_CurrentPercent.setText('---')
        self.progressBar_All.setRange(0, 5)

        self.create_file_list_task = RunCreateFileList(directory, recursiveBool, reconvertBool, thumbnailsBool)
        self.create_file_list_task.task_result.connect(self.create_file_list_results)
        self.create_file_list_task.task_finished.connect(self.create_file_list_finished)

        self.create_file_list_task.start()

    def create_file_list_results(self, result):
        if result[0] == 'self.file_list':
            self.file_list = result[1]
        elif result[0] == 'self.file_list_reconvert':
            self.file_list_reconvert = result[1]
        elif result[0] == 'self.file_list_thumbnails':
            self.file_list_thumbnails = result[1]
        else:
            print('\nUnexpected value:')
            pprint(result)

    def create_file_list_finished(self):
        print('create_file_list_finished')
        self.set_status('Step 1: Creating File List - Complete')
        self.progressBar_Current.setRange(0, 100)

        # Start the get_media_info task
        self.get_media_info()

    # End create file list functions

    # Start get media info functions

    def get_media_info(self):
        self.set_status('Step 2: Getting Media Info')

        self.get_media_info_task = RunGetMediaInfo(self.file_list_reconvert, self.mediainfo_path)
        self.get_media_info_task.task_result.connect(self.get_media_info_results)
        self.get_media_info_task.task_finished.connect(self.get_media_info_finished)
        self.get_media_info_task.task_folder.connect(self.set_folder)
        self.get_media_info_task.task_file.connect(self.set_file)

        self.progressBar_Current.setRange(0, 0)
        self.label_CurrentPercent.setText('---')
        self.get_media_info_task.start()

    def get_media_info_results(self, result):
        print('\n\nget_media_info_results')
        pprint(result)
        self.file_list_reconvert = result

    def get_media_info_finished(self):
        print('\n\nget_media_info_finished')
        self.progressBar_Current.setRange(0, 100)
        self.set_status('Step 2: Getting Media Info - Complete')

        # Start the number of frames task
        self.get_number_frames()

    # End get media info functions

    # Start get number of frames functions

    def get_number_frames(self):
        self.set_status('Step 3: Getting Number of Frames')

        self.get_number_frames_task = RunGetNumFrames(self.file_list_reconvert, self.ffprobe_path)
        self.get_number_frames_task.task_result.connect(self.get_number_frames_results)
        self.get_number_frames_task.task_finished.connect(self.get_number_frames_finished)
        self.get_number_frames_task.task_folder.connect(self.set_folder)
        self.get_number_frames_task.task_file.connect(self.set_file)
        self.get_number_frames_task.task_AllFraction.connect(self.set_AllFraction)
        self.get_number_frames_task.task_AllPercent.connect(self.set_AllPercent)

        self.progressBar_Current.setRange(0, 0)
        self.label_CurrentPercent.setText('---')
        self.progressBar_All.setRange(0, 100)
        self.get_number_frames_task.start()

    def get_number_frames_results(self, result):
        print('\n\nget_number_frames_results')
        pprint(result)
        self.file_list_reconvert = result

    def get_number_frames_finished(self):
        print('\n\nget_media_info_finished')
        self.set_status('Step 3: Getting Number of Frames - Complete')
        self.progressBar_Current.setRange(0, 100)

        # Start the create mp4 function
        self.create_mp4()

    # End get number of frames functions

    # Start create mp4 functions

    def create_mp4(self):
        self.set_status('Step 4: Creating MP4 Files')

        stabilizeBool = self.checkBox_Stabilize.checkState()

        self.create_mp4_task = RunCreateMP4(self.file_list_reconvert, self.ffmpeg_path, stabilizeBool)
        self.create_mp4_task.task_finished.connect(self.create_mp4_finished)
        self.create_mp4_task.task_folder.connect(self.set_folder)
        self.create_mp4_task.task_file.connect(self.set_file)
        self.create_mp4_task.task_AllFraction.connect(self.set_AllFraction)
        self.create_mp4_task.task_AllPercent.connect(self.set_AllPercent)
        self.create_mp4_task.task_CurrentPercent.connect(self.set_CurrentPercent)

        self.create_mp4_task.start()

    def create_mp4_finished(self):
        print('\n\ncreate_mp4_finished')
        self.set_status('Step 4: Creating MP4 - Complete')

        # Run thumbnail function
        self.create_thumbnails()

    # End create mp4 functions

    # Start create thumbnail functions

    def create_thumbnails(self):
        self.set_status('Step 5: Creating Thumbnails')

        recreatethumbsBool = self.checkBox_Thumbnails.checkState()

        self.create_thumbnails_task = RunCreateThumbnails(self.file_list_thumbnails, self.mediainfo_path,
                                                          self.ffmpeg_path, self.imagemagick_path,
                                                          self.convert_path, self.composite_path, recreatethumbsBool)
        self.create_thumbnails_task.task_finished.connect(self.create_thumbnails_finished)
        self.create_thumbnails_task.task_folder.connect(self.set_folder)
        self.create_thumbnails_task.task_file.connect(self.set_file)
        self.create_thumbnails_task.task_AllFraction.connect(self.set_AllFraction)
        self.create_thumbnails_task.task_AllPercent.connect(self.set_AllPercent)
        self.create_thumbnails_task.task_CurrentPercent.connect(self.set_CurrentPercent)

        self.create_thumbnails_task.start()

    def create_thumbnails_finished(self):
        print('\n\ncreate_thumbnails_finished')
        self.set_status('Step 5: Creating Thumbnails - Complete')

    # End create thumbnail functions


class RunCreateFileList(QtCore.QThread):
    task_finished = QtCore.Signal()
    task_result = QtCore.Signal(list)
    # task_file_list = QtCore.Signal(list)
    # task_file_list_reconvert = QtCore.Signal(list)
    # task_file_list_thumbnails = QtCore.Signal(list)

    def __init__(self, directory, recursiveBool, reconvertBool, thumbnailsBool):
        QtCore.QThread.__init__(self)
        self.directory = directory
        self.recursiveBool = recursiveBool
        self.reconvertBool = reconvertBool
        self.thumbnailsBool = thumbnailsBool

        self.file_list = []
        self.file_list_reconvert = []
        self.file_list_thumbnails = []

    def run(self):
        video_ext = ['.avi', '.mpg', '.mov', '.wmv']

        if self.recursiveBool == QtCore.Qt.Checked:
            for root, sub_folders, files in os.walk(self.directory):
                for f in files:
                    if os.path.splitext(f)[1].lower() in video_ext:
                        self.file_list.append({'name': os.path.realpath(os.path.join(root, f))})

        else:
            filenames = next(os.walk(self.directory))[2]
            for f in filenames:
                if os.path.splitext(f)[1].lower() in video_ext:
                    self.file_list.append({'name': os.path.realpath(os.path.join(root, f))})

        # Send a result back to the main thread
        self.task_result.emit(['self.file_list', self.file_list])

        if self.reconvertBool == QtCore.Qt.Checked:
            self.file_list_reconvert = self.file_list
        else:
            self.file_list_reconvert = [x for x in self.file_list if self.cull_list(x, '.mp4')]

        # Send a result back to the main thread
        self.task_result.emit(['self.file_list_reconvert', self.file_list_reconvert])

        if self.thumbnailsBool == QtCore.Qt.Checked:
            self.file_list_thumbnails = self.file_list
        else:
            self.file_list_thumbnails = [x for x in self.file_list if self.cull_list(x, '.jpg')]

        # Send a result back to the main thread
        self.task_result.emit(['self.file_list_thumbnails', self.file_list_thumbnails])

        # Tell the main thread that we're done
        self.task_finished.emit()

    def cull_list(self, f='', ext=''):
        if f != '':
            test_name = os.path.splitext(f['name'])[0] + ext
            if os.path.isfile(test_name):
                return False
            else:
                return True


class RunGetMediaInfo(QtCore.QThread):
    task_finished = QtCore.Signal()
    task_result = QtCore.Signal(list)

    task_folder = QtCore.Signal(str)
    task_file = QtCore.Signal(str)

    def __init__(self, file_list, media_info_path):
        QtCore.QThread.__init__(self)
        self.file_list = file_list
        self.media_info_path = media_info_path

    def run(self):
        print('RunGetMediaInfo')

        for f in self.file_list:
            self.task_folder.emit(os.path.split(f['name'])[0])
            self.task_file.emit(os.path.split(f['name'])[1])

            duration_found = False
            duration = 0

            media_info = os.popen(self.media_info_path + ' "' + f['name'] + '"').readlines()

            for line in media_info:
                try:
                    if line.split(' ')[0] == 'Rotation':
                        print(line.split())
                        rotation = line.split()[2][:-1]
                        f['rotation'] = rotation

                    elif line.split(' ')[0] == 'Duration':
                        duration_line = line.split(': ')[1]
                        if not duration_found:
                            for chunk in duration_line.split(' '):
                                match = re.match(r"([0-9]+)([a-z]+)", chunk, re.I)
                                if match:
                                    items = match.groups()

                                    if items[1] == 'hr':
                                        duration += float(items[0]) * 3600

                                    elif items[1] == 'mn':
                                        duration += float(items[0]) * 60

                                    elif items[1] == 's':
                                        duration += float(items[0])

                                    elif items[1] == 'ms':
                                        duration += float(items[0]) / 1000

                                f['duration'] = duration

                                duration_found = True

                except Exception as e:
                    msgBox = QtGui.QMessageBox()
                    msgBox.setText(e)
                    msgBox.exec_()

        self.task_result.emit(self.file_list)
        self.task_finished.emit()


class RunGetNumFrames(QtCore.QThread):
    task_finished = QtCore.Signal()
    task_result = QtCore.Signal(list)

    task_folder = QtCore.Signal(str)
    task_file = QtCore.Signal(str)

    task_AllFraction = QtCore.Signal(str)
    task_AllPercent = QtCore.Signal(float)

    def __init__(self, file_list, ffprobe_path):
        QtCore.QThread.__init__(self)
        self.file_list = file_list
        self.ffprobe_path = ffprobe_path

    def run(self):
        print('RunGetNumFrames')

        file_count = 1

        for f in self.file_list:
            self.task_folder.emit(os.path.split(f['name'])[0])
            self.task_file.emit(os.path.split(f['name'])[1])

            percentage = float(file_count) / float(len(self.file_list))
            self.task_AllFraction.emit(str(file_count) + ' / ' + str(len(self.file_list)))
            self.task_AllPercent.emit(percentage)

            ffprobe_info = os.popen(self.ffprobe_path + ' -i "' + f['name'] + '" -show_frames').readlines()

            frames = 0

            for line in ffprobe_info:
                if line == 'pict_type=P\n':
                    frames += 1

            f['frames'] = frames

            file_count += 1

        self.task_result.emit(self.file_list)
        self.task_finished.emit()


class RunCreateMP4(QtCore.QThread):
    task_finished = QtCore.Signal()

    task_folder = QtCore.Signal(str)
    task_file = QtCore.Signal(str)

    task_AllFraction = QtCore.Signal(str)
    task_AllPercent = QtCore.Signal(float)

    task_CurrentPercent = QtCore.Signal(float)

    def __init__(self, file_list, ffmpeg_path, stabilize):
        QtCore.QThread.__init__(self)
        self.file_list = file_list
        self.ffmpeg_path = ffmpeg_path
        self.stabilize = stabilize

    def run(self):
        print('RunCreateMP4')

        file_count = 1

        for f in self.file_list:
            self.task_folder.emit(os.path.split(f['name'])[0])
            self.task_file.emit(os.path.split(f['name'])[1])

            percentage = float(file_count) / float(len(self.file_list))
            self.task_AllFraction.emit(str(file_count) + ' / ' + str(len(self.file_list)))
            self.task_AllPercent.emit(percentage)

            output = os.path.splitext(f['name'])[0] + '.mp4'

            # Remove file if it is found
            # If reconvert checkbox is unchecked, the file should have already been removed from self.file_list
            if os.path.isfile(output):
                os.remove(output)

            transpose = ''
            if 'rotation' in f:
                if f['rotation'] == '90':
                    transpose = '-vf "transpose=1"'
                elif f['rotation'] == '180':
                    transpose = '-vf hflip,vflip'
                elif f['rotation'] == '270':
                    transpose = '-vf "transpose=2"'

            cmd = ''
            if self.stabilize == QtCore.Qt.Checked:
                # if transpose == '':
                #     transpose = '-vf'
                cmd = self.ffmpeg_path + ' -i "' + f['name'] + '" ' + transpose + ' -vf vidstabdetect=stepsize=6:shakiness=8:accuracy=9:result=transform_vectors.trf -f null -'

                print(cmd)

                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           universal_newlines=True)
                for line in process.stdout:
                    line_split = line.split()
                    if line_split[0] == 'frame=':
                        curr_percent = float(line_split[1]) / float(f['frames']) / 2
                        if curr_percent > 1:
                            curr_percent = 1
                        self.task_CurrentPercent.emit(curr_percent)

                cmd = self.ffmpeg_path + ' -i "' + f['name'] + '" -vf vidstabtransform=input=transform_vectors.trf:zoom=1:smoothing=30,unsharp=5:5:0.8:3:3:0.4 -vcodec libx264 -preset slow -tune film -crf 18 -acodec copy "' + output + '"'
                print(cmd)

                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                               universal_newlines=True)
                for line in process.stdout:
                    line_split = line.split()
                    if line_split[0] == 'frame=':
                        curr_percent = 0.5 + float(line_split[1]) / float(f['frames']) / 2
                        if curr_percent > 1:
                            curr_percent = 1
                        self.task_CurrentPercent.emit(curr_percent)

                if os.path.isfile('transform_vectors.trf'):
                    os.remove('transform_vectors.trf')


            else:
                cmd = self.ffmpeg_path + ' -i "' + f['name'] + '" ' + transpose + ' -strict experimental -metadata:s:v:0 rotate=0 "' + output + '"'

                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                for line in process.stdout:
                    line_split = line.split()
                    if line_split[0] == 'frame=':
                        curr_percent = float(line_split[1]) / float(f['frames'])
                        if curr_percent > 1:
                            curr_percent = 1
                        self.task_CurrentPercent.emit(curr_percent)

            originaltime = os.path.getmtime(f['name'])
            os.utime(output, (originaltime, originaltime))

            file_count += 1

        self.task_finished.emit()


class RunCreateThumbnails(QtCore.QThread):
    task_finished = QtCore.Signal()

    task_folder = QtCore.Signal(str)
    task_file = QtCore.Signal(str)

    task_AllFraction = QtCore.Signal(str)
    task_AllPercent = QtCore.Signal(float)

    task_CurrentPercent = QtCore.Signal(float)

    def __init__(self, file_list, media_info_path, ffmpeg_path, im_path, convert_path, composite_path, recreateThumbs):
        QtCore.QThread.__init__(self)
        self.file_list = file_list
        self.media_info_path = media_info_path
        self.ffmpeg_path = ffmpeg_path
        self.imagemagick_path = im_path
        self.convert_path = convert_path
        self.composite_path = composite_path
        self.recreateThumbs = recreateThumbs

    def run(self):
        print('RunCreateThumbnails')

        file_count = 1

        for f in self.file_list:
            self.task_folder.emit(os.path.split(f['name'])[0])
            self.task_file.emit(os.path.split(f['name'])[1])

            percentage = float(file_count) / float(len(self.file_list))
            self.task_AllFraction.emit(str(file_count) + ' / ' + str(len(self.file_list)))
            self.task_AllPercent.emit(percentage)

            output = os.path.splitext(f['name'])[0] + '.jpg'
            converted_movie = os.path.splitext(f['name'])[0] + '.mp4'

            # Remove file if it is found
            # If recreate thumbnails checkbox is unchecked, the file should have already been removed from self.file_list
            if os.path.isfile(output):
                os.remove(output)

            media_info = os.popen(self.media_info_path + ' "' + f['name'] + '"').readlines()

            width = None
            height = None

            for line in media_info:
                line_split = line.split(':')
                try:
                    if line_split[0].lower().rstrip() == 'width':
                        width = line_split[1]
                    elif line_split[0].lower().rstrip() == 'height':
                        height = line_split[1]
                except:
                    pass

            width = ''.join(width.split(' ')[1:-1])
            height = ''.join(height.split(' ')[1:-1])

            min_dimension = str(int(min(float(width), float(height))))

            getphoto = self.ffmpeg_path + ' -i "' + converted_movie + '" -ss 00:00:01 -vframes 1 "' + output + '"'

            os.system(getphoto)

            im_command = ''
            im_command2 = ''
            if os.name == 'posix':
                im_command = self.convert_path + ' play.png -resize ' + min_dimension + 'x' + min_dimension + ' play_temp.png'
                im_command2 = self.composite_path + ' -gravity center play_temp.png "' + output + '" "' + output + '"'

            else:
                im_command = imagemagick_path + '\convert.exe play.png -resize ' + min_dimension + 'x' + min_dimension + ' play_temp.png'
                im_command2 = imagemagick_path + '\composite.exe -gravity center play_temp.png "' + output + '" "' + output + '"'

            os.system(im_command)
            os.system(im_command2)
            os.remove('play_temp.png')

            originaltime = os.path.getmtime(f['name'])
            os.utime(output, (originaltime, originaltime))

            file_count += 1

        self.task_finished.emit()


##############
# TESTING
#############
#     def ok_pushed_test(self):
#         print('close pushed')
#         self.progressBar_Current.setRange(0, 0)
#         self.progressBar_All.setRange(0, 5)
#         self.LongTask2 = RunTask2()
#         self.LongTask2.updateProgress.connect(self.setProgress)
#         self.LongTask2.taskFinished.connect(self.onFinished)
#         self.LongTask2.start()
#
#     def setProgress(self, progress):
#         self.progressBar_All.setValue(progress)
#
#     def onFinished(self):
#         self.progressBar_Current.setRange(0, 100)
#         print('done')
#
#
# class RunTask2(QtCore.QThread):
#     taskFinished = QtCore.Signal()
#
#     updateProgress = QtCore.Signal(int)
#
#     def run(self):
#         i = 1
#         while i < 6:
#             print('Run2' + str(i))
#             # self.progressBar_All.setValue(i)
#             self.updateProgress.emit(i)
#             time.sleep(1)
#             i += 1
#         self.taskFinished.emit()

################################
# End Testing
################################


def main():
    app = QtGui.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
