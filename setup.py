import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfviewer",
    version="0.0.2",
    author="Fatih Mete",
    author_email="fatihmete@live.com",
    description="A data view tool for pandas data frames working on Jupyter Notebook or IPython.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fatihmete/dfviewer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   install_requires=[
          'PyQt5', 'numpy'
   ],
   python_requires='>=3.6',
)
