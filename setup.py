from setuptools import setup, find_packages
import sys

sys.argv.append('install')

setup(
    name = "eudtrg",
    version = "0.2-r3",
    packages = find_packages(),
    package_data = {
        '': ['*.dll', '*.lst'],
    },

    # metadata for upload to PyPI
    author = "Trgk",
    author_email = "whyask37@naver.com",
    description = "EUD Trigger generator",
    license = "New BSD License",
    keywords = "starcraft trigger eud",
    url = "http://blog.naver.com/whyask37/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)

