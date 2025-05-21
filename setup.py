from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip()
        for line in fh.read().split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="healph_articles",
    version="0.1.0",
    author="Rafael Araújo",
    author_email="seu.email@exemplo.com",
    description="Gerador de Artigos de Saúde com IA usando CrewAI e Streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/araujobazilio/healph_articles",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    keywords="ai health medical article generation crewai streamlit",
    project_urls={
        "Bug Reports": "https://github.com/araujobazilio/healph_articles/issues",
        "Source": "https://github.com/araujobazilio/healph_articles",
    },
    include_package_data=True
)
