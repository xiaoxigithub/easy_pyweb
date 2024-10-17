import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# easy_pyweb项目
setuptools.setup(
    name="easy_pyweb",
    version="0.0.1",
    author="xiaoxi",
    author_email="xiaoxiggnet@gmail.com",
    url="https://github.com/xiaoxigithub",
    description="web helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "requests",
        "playwright",
    ],
    python_requires=">=3.6",
)
