# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['eliminarfondo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icono_app.ico', '.'),
        ('icon_cargar.png', '.'),
        ('icon_eliminar.png', '.'),
        ('icon_guardar.png', '.'),
        ('icon_borrar.png', '.'),
        ('icon_editar.png', '.'),
        ('icon_restaurar.png', '.'),
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
    name='eliminarfondo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = sin consola, True = con consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icono_app.ico'],
)

