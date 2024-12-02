# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/client/main.py'],  # Entry script
    pathex=['/Users/jp/Desktop/projects/pysnmp/src'],  # Path to the src directory (absolute path)
    binaries=[],
    datas=[('src/client/agents', 'agents'), ('src/client/components', 'components'), ('src/client/helpers', 'helpers')],  # Include the agents directory as 'agents' in the bundle
    hiddenimports=[
    'agents.transaction',
    'components.target',
    'components.varbinds',
    'components.notification',
    'components.save_config',
    'components.load_config',
    'helpers.validation',
    'pysnmp.hlapi.asyncio',
    'json'
    ],
    hookspath=[],  # Specify hooks if necessary
    runtime_hooks=[],  # Runtime hooks if required
    excludes=[],  # Exclude unnecessary modules
    noarchive=True,  # Avoid archiving the Python code
    optimize=0,  # No optimization
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
