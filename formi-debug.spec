# -*- mode: python ; coding: utf-8 -*-

# PyInstaller command during development
#  -> pyinstaller formi-debug.spec --distpath release

__version__ = '0.2.1-debug'
__appname__ = 'formi'
block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['C:\\Users\\gerolbado\\Documents\\GitHub\\Formi'],
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
          name=f'{__appname__}-{__version__}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name=__appname__)
