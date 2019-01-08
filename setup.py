import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graph_api",
    version="0.0.1",
    author="daryasary",
    author_email="hosein@inprobes.com",
    description="Python sdk for Instagram graph api(facebook version)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daryasary/instagram-graph-api",
    # todo: requests is not going to be detected
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Apache",
    ],
)
