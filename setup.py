from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in custom_srg/__init__.py
from custom_srg import __version__ as version

setup(
	name="custom_srg",
	version=version,
	description="Custom Development by SRG",
	author="SRG",
	author_email="sagar1ratan1garg1@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
