# Define the Analysis step
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        # Add the python313.dll file from your Python directory
        ('C:\\Users\\karan\\AppData\\Local\\Programs\\Python\\Python313\\python313.dll', '_internal')
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Define the PYZ (Python bytecode archive) step
pyz = PYZ(a.pure)

# Define the EXE step
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Define the COLLECT step
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
    tree='_internal',  # Ensure the DLL goes into the _internal folder in the dist
)
