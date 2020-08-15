# -*- mode: python ; coding: utf-8 -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['C:\\Users\\PIPE_PC\\Documents\\UNIVERSIDAD\\TESIS\\epic-sns-5G\\prototipo_v3\\gui.py'],
             pathex=['C:\\Users\\PIPE_PC\\Documents\\UNIVERSIDAD\\TESIS\\epic-sns-5G\\prototipo_v3\\5Gsimulatorapp'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('C:\\Users\\PIPE_PC\\Documents\\UNIVERSIDAD\\TESIS\\epic-sns-5G\\prototipo_v3\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               upx_exclude=[],
               name='gui')
