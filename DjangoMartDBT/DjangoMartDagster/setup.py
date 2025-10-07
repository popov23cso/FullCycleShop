from setuptools import find_packages, setup

setup(
    name="DjangoMartDagster",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "DjangoMartDagster": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-core<1.11",
        "dbt-duckdb<1.11",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)