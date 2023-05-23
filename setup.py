import io
import re

from setuptools import find_packages
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with io.open(path.join(this_directory, "app", "__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="albumapp",
    version=version,
    url="https://reportbro.com",
    project_urls={
        "Documentation": "https://github.com/jobsta/albumapp-flask",
        "Code": "https://github.com/jobsta/albumapp-flask",
        "Issue tracker": "https://github.com/jobsta/albumapp-flask/issues",
    },
    license="MIT",
    maintainer="jobsta",
    maintainer_email="contact@jobsta.at",
    description="Album Demo-App for Flask",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.5",
    install_requires=[
        "flask==2.3.2",
        "Werkzeug==2.3.4",
        "Jinja2==3.1.2",
        "itsdangerous==2.1.2",
        "click==8.1.3",
        "python-dotenv==1.0.0",
        "Flask-Babel==3.1.0",
        "reportbro-lib>=3.2.0",
        "SQLAlchemy==2.0.15",
        "requests==2.31.0"
    ],
    entry_points={"console_scripts": ["flask = flask.cli:main"]},
)
