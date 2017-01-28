# -*- mode: python -*-
a = Analysis(['videoconvert.py'],
             #pathex=['C:\\Projects\\CDMConverter'],
             pathex=[''],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

# a.datas += [(r'ColdPD.PNG', r'ColdPD.PNG', 'DATA')]

for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='VideoConvert_0.1.0.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
