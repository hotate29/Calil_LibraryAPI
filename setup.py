from setuptools import setup,find_packages

setup(
    name="calilapi",
    version="0.0.1",
    install_requires=["requests"],
    packages=find_packages("src"),
    package_dir={"":"src"}
)
