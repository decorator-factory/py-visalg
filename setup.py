import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visalg-decorator-factory",
    version="1.0.0",
    author="decorator-factory",
    author_email="trkbobo@yandex.ru",
    description="Algorithm visualization library for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/decorator-factory/py-visalg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)