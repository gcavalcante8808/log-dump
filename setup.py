from distutils.core import setup
try:
    import py2exe
except ImportError:
    py2exe = None

setup(name='log-dump',
      version='0.1',
      scripts=['log_dump.py', ],
      author='Gabriel Abdalla Cavalcante',
      author_email='gabriel.cavalcante88@gmail.com',
      url='https://github.com/gcavalcante8808',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache License',
        'Operating System :: Win32 :: Windows',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
      ]
)
