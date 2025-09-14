from setuptools import setup, find_packages

setup(
    name="nkflow",  # Updated package name  
    version="0.1.0",
    author="Nitin Kaira",  # Updated author name
    author_email="nkaira784@gmail.com",  # Updated author email
    description="Generate, save, and optionally run AI-generated code using LangChain LLMs.",
    packages=find_packages(),
    install_requires=[
        "langchain-core>=0.0.208",
        "langchain-community>=0.0.35",
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)