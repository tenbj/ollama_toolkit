from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ollama_toolkit",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个用于调用Ollama模型的Python工具包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ollama_toolkit",  # 替换为实际的仓库URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.0',
    ],
    entry_points={
        'console_scripts': [
            'ollama-tool=ollama_toolkit.cli:main',
        ],
    },
)