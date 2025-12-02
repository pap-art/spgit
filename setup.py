"""
Setup script for spgit - Git for Spotify Playlists
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="spgit",
    version="1.0.0",
    author="spgit contributors",
    author_email="",
    description="Git for Spotify Playlists - A complete version control system for Spotify playlists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spgit",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Version Control",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "spotipy>=2.23.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spgit=spgit.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="spotify git version-control playlist music",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/spgit/issues",
        "Source": "https://github.com/yourusername/spgit",
    },
)
