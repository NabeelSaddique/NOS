from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Package metadata
setup(
    name="nos-assessment-tool",
    version="1.0.0",
    author="Muhammad Nabeel Saddique",
    author_email="nabeel.saddique@kemu.edu.pk",
    description="Newcastle-Ottawa Scale Assessment Tool for Systematic Reviews and Meta-Analyses",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/nos-assessment-tool",
    project_urls={
        "Bug Reports": "https://github.com/username/nos-assessment-tool/issues",
        "Source": "https://github.com/username/nos-assessment-tool",
        "Documentation": "https://github.com/username/nos-assessment-tool/docs",
        "Nibras Research Academy": "https://nibrasresearch.com"
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
        "jupyter": [
            "jupyter>=1.0.0",
            "ipykernel>=6.25.0",
            "ipywidgets>=8.1.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "sphinx>=7.0.0",
            "jupyter>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "nos-tool=src.main:main",
            "nos-batch=scripts.batch_assessment:main",
            "nos-validate=scripts.validate_data:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.csv", "*.md", "*.txt", "*.yaml", "*.yml"],
        "data": ["templates/*", "examples/*"],
        "assets": ["images/*", "templates/*"],
    },
    keywords=[
        "systematic-review",
        "meta-analysis", 
        "newcastle-ottawa-scale",
        "risk-of-bias",
        "evidence-based-medicine",
        "research-methodology",
        "quality-assessment",
        "observational-studies",
        "cohort-studies",
        "case-control-studies",
        "cross-sectional-studies",
        "robvis",
        "streamlit",
        "visualization"
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    maintainer="Muhammad Nabeel Saddique",
    maintainer_email="nabeel.saddique@kemu.edu.pk",
)
