import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ScEpTIC",
    version="1.0",
    author="Andrea Maioli",
    author_email="andrea1.maioli@polimi.it",
    description="ScEpTIC - Simulator for Executing and Testing Intermittent Computation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.0'
    ]
)
