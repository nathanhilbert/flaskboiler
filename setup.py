import os
from setuptools import setup, find_packages


PKG_ROOT = os.path.abspath(os.__file__)


def files_in_pkgdir(pkg, dirname):
    pkgdir = os.path.join(PKG_ROOT, *pkg.split('.'))
    walkdir = os.path.join(pkgdir, dirname)
    walkfiles = []
    for dirpath, _, files in os.walk(walkdir):
        fpaths = (os.path.relpath(os.path.join(dirpath, f), pkgdir)
                  for f in files)
        walkfiles += fpaths
    return walkfiles


def package_filter(pkg):
    """
    Filter packages so that we exclude test cases but include regular test
    objects available in openspending.tests' modules (all test cases are
    in subdirectories).
    """

    # We want to include openspending.tests but not its subpackages
    # Hence we only check for things starting with openspending.tests.
    # (note the trailing period to denote subpackages)
    return not pkg.startswith('flaskboiler.tests.')

setup(
    name='flaskboiler',
    version='0.17',
    description='FlaskBoiler',
    author='nathanhilbert',
    author_email='',
    url='',
    install_requires=[
    ],
    setup_requires=[],

    packages=filter(package_filter, find_packages()),
    namespace_packages=['flaskboiler'],
    package_data={
        'flaskboiler': (
            files_in_pkgdir('flaskboiler', 'static') +
            files_in_pkgdir('flaskboiler', 'templates')
        )
    },
    test_suite='nose.collector',

    zip_safe=False,

    entry_points={
        'console_scripts': [
            'manager = flaskboiler.command:main',
        ]
    },

    message_extractors={
        'flaskboiler': [('**.py', 'python', None),
                         ('templates/**.html', 'jinja2', None),
                         ('static/**', 'ignore', None),
                         ]
        },
)
