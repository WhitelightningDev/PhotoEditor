# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['realesrgan_gui.py'],
    pathex=['PhotoEditor'],
    binaries=[
        ('realesrgan/realesrgan-ncnn-vulkan.exe', 'realesrgan'),  # Adjusted path
    ],
    datas=[
     ('assets', 'assets'),  # Ensures assets folder is included
        ('realesrgan', 'realesrgan'),  # Ensure this copies the entire folder
        ('realesrgan/models', 'realesrgan/models'),  # Ensure this is correct if models are inside realesrgan
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PhotoEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Keep console to see errors or use False and log output to a file
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/magic-wand.ico',  # Add your icon file here
)

