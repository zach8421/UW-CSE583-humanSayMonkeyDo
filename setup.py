from setuptools import find_packages, setup

setup(
    name="CSE583_humanSayMonkeyDo",
    version="0.1.0",
    description="CSE583 Human Say Monkey Do project package.",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
)
