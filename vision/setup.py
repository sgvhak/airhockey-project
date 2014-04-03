from setuptools import setup

setup(
    name='SGVHAK Air Hockey Robot',
    version='0.1',
    author='Omwah Oyeh',
    author_email='omwah@oyeh.org',
    license='GPL v3',
    description='Vision, physics and simulation software for SGVHAK Air Hockey Robot',
    long_description=open('README.rst').read(),
    url='https://github.com/sgvhak/airhockey-project',
    packages=['hhr'],
    scripts=['hhr.py',],
    install_requires=[
        'numpy >= 1.7.1',
        'pymunk >= 4.0.0',
        'pygame >= 1.9.1',
    ],
)
