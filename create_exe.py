import os
import sys

# path_to_pyinstaller = 'C:\Portable_Software\pyinstaller-2.0'

# spec_path = 'VideoConvert.spec'

cmd = sys.executable + ' ' + 'C:\Portable_Software\pyinstaller-2.1\pyinstaller.py -y -w VideoConvert.spec'
# cmd = sys.executable + ' ' + 'C:\Portable_Software\pyinstaller-2.1\pyinstaller.py -y VideoConvert.spec'
print(cmd)

os.system(cmd)