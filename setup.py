from distutils.core import setup

current_version = '0.1.0'

setup(
  name = 'lib-powermate',
  packages = ['powermate'],
  version = current_version,
  description = 'Library to use Griffin PowerMate wheels',
  long_description = '''

Library to use Griffin PowerMate wheels.

Please refer to the GitHub documentation for more information.

  ''',
  author = 'Enrico Lamperti',
  author_email = 'elamperti@users.noreply.github.com',
  license='GNU GPL v2',
  url = 'https://github.com/elamperti/lib-powermate',
  download_url = 'https://github.com/elamperti/lib-powermate/archive/' + current_version + '.tar.gz',
  keywords = ['griffin', 'powermate', 'library', 'controller', 'driver', 'events'],
  classifiers = [],
)
