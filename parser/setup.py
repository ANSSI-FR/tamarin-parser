import setuptools

setuptools.setup(
    name = "tamarinparser",
    version = "0.0.1",
    author = "Ano Nymous",
    author_email = "ano@nymous.com",
    description = "Parser for Tamarin files",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    scripts = ['scripts/tamparse.py']
)

