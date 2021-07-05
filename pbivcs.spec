# -*- mode: python -*-
from PyInstaller.building.build_main import EXE, PYZ, Analysis
from PyInstaller.utils.hooks import copy_metadata

# from . import cli

datas = []
datas += copy_metadata("powerbi_vcs")

block_cipher = None
a = Analysis(
    scripts=["cli.py"],
    # scripts=[cli.__file__],
    # pathex=["src/powerbi_vcs"],
    # binaries=[],
    binaries=None,
    # datas=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    # [],
    name="pbivcs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # upx_exclude=[],
    runtime_tmpdir=None,
    # console=False,
    console=True,
    # icon='.ico'
)
