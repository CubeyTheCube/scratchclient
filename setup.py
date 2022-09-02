import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scratchclient",
    packages=["scratchclient"],
    version="1.0.1",
    license="MIT",
    description="A scratch API wrapper for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CubeyTheCube",
    author_email="turtles142857@gmail.com",
    url="https://github.com/CubeyTheCube/scratchclient",
    download_url="https://github.com/CubeyTheCube/scratchclient/archive/v_10.1.tar.gz",
    keywords=["scratch", "api"],
    install_requires=["requests"],
    extras_require={"fast": ["numpy", "wsaccel"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
