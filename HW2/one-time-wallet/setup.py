from distutils.core import setup, Extension

extension_mod = Extension('revers_state', ['share.c'])
setup(name = 'revers_state', ext_modules=[extension_mod])
