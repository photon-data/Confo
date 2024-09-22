import pathlib
from setuptools import setup,find_packages
import os
# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# The text of the README file
with open(HERE + "/README.md", encoding='utf-8') as f:
    README = f.read()

with open(HERE +'/requirements.txt') as f:
    required = f.read().splitlines()
    print(required)
    setup(
        name="confo2",
        version="0.1.0",
        description="Confo is a configuration manager, built to support multiple backend systems",
        long_description_content_type="text/markdown",
        long_description=README,
        url="https://github.com/sambe-consulting/confo",
        author="Sambe Consulting",
        author_email="development@sambe.co.za",
        license="Apache License 2.0",
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python :: 3",
        ],
        packages=find_packages(exclude=("tests",)),
        include_package_data=True,
        install_requires=required,
        python_requires='>=3.6',  # Specify compatible Python versions

    )
# This call to setup() does all the work