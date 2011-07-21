from distutils.core import setup

version = __import__('django_odesk').get_version()

setup(name='django-odesk',
      version=version,
      description='oDesk API integration for Django',
      long_description='',
      author='Oleksiy Solyanyk',
      author_email='solex@odesk.com',
      packages = ['django_odesk','django_odesk.auth', 'django_odesk.core', 'django_odesk.conf'],
      install_requires = ['python-odesk>=0.1.2', ],
      classifiers=['Development Status :: 1 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],)
