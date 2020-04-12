import re
from pathlib import Path
from setuptools import setup, find_packages

__folder__ = Path(__file__).parent


def read(*path_leaves, **kwargs):
    kwargs.setdefault('encoding', "utf-8")
    with Path(__folder__, *path_leaves).open(**kwargs) as f:
        return f.read()


def find_version(*path_leaves):
    version_file = read(*path_leaves)
    version_match = re.search(r"^__version__ = (['\"])(.*?)\1", version_file, re.M)
    if version_match:
        return version_match.group(2)
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="airpods-helper",
    packages=find_packages(exclude=["tests"]),
    version=find_version("airpods_helper", "__init__.py"),
    description="Small utility to automate Apple Airpods connection process",
    long_description=read("README.md"),
    url="https://github.com/thevar1able/airpods-helper",
    author="thevar1able",
    author_email="var1able@var1able.ru",
    license='MIT',
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    keywords=["airpods", "dbus", "bluetooth", "bluez", "mpris"],
    entry_points={
        'console_scripts': [
            "airpods-helper=airpods_helper.__main__:main",
        ],
    },
    install_requires=["PyGObject", "pydbus"],
    python_requires=">=3.6",
)