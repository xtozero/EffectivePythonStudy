from distutils.core import setup, Extension
from distutils import msvc9compiler
msvc9compiler.VERSION = 14.0

mod = Extension('Module', sources=['main.cpp'])
setup(name = 'Module',
      version='1.0',
      description='extension module',
      ext_modules=[mod],
)
