"""setup.py file.

Defines the requirements and configuration for packaging and
running the application.
"""
import setuptools

requirements = ["flask==3.1.0",
                "flask-cors==5.0.1",
                "flask-restful==0.3.10",
                "google-genai==1.16.1",
                "openai==1.79.0",
                "pytest==8.4.2"]

setuptools.setup(
    name="DeCoMi",
    version="1",
    author="Annemae van de Hoef",
    author_email="annemae.vandehoef@hu.nl",
    description="DeCoMi Prototype Back-end & Front-end",
    url="https://github.com/Annemae/DeCoMi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows 11",
    ],
    install_requires=requirements,
    python_requires='>=3.13.2',
)
