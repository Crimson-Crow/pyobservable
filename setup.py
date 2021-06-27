from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyobservable',
    version='1.0.0',
    description='TODO',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Crimson-Crow/TODO',
    author='Crimson-Crow',
    author_email='github@crimsoncrow.dev',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='TODO',
    license='MIT',
    python_requires='>=3.6, <4',
    py_modules=['pyobservable'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Crimson-Crow/TODO/issues',
        'Source': 'https://github.com/Crimson-Crow/TODO',
    },
)