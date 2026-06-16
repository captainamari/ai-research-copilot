from setuptools import find_packages, setup


setup(
    name="ai-research-copilot",
    version="0.1.0",
    package_dir={
        "research_copilot": "src/research_copilot",
        "apps": "apps",
    },
    packages=find_packages(where="src") + find_packages(include=["apps", "apps.*"]),
    python_requires=">=3.11",
)
