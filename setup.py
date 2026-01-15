from setuptools import find_packages, setup

setup(
    name="imperial-painter",
    version="1.1.0",
    include_package_data=True,
    packages=find_packages(),

    install_requires=[
        "dj-database-url==3.1.0",
        "Django==6.0.1",
        "django-extensions==4.1",
        "lxml==6.0.2",
        "openpyxl==3.1.5",
        "psycopg2-binary==2.9.11",
    ],

    author="Adam Thomas",
    description="A tool for generating prototype cards from Excel files and Django templates",
    url="https://github.com/adam-thomas/imperial-painter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
