from setuptools import setup, find_packages
import sys, os

version = "0.1"

setup(
    name="ipsql",
    version=version,
    description="Intelligent PostgreSQL shell.",
    author="Andrey Popp",
    author_email="8mayday@gmail.com",
    license="3BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "psycopg2",
        "rl",
        "sqlparse"
    ],
    entry_points="""
    [console_scripts]
    ipsql = ipsql.cli:main
    """,
    )
