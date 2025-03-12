import setuptools

requirements = ["flask==3.1.0",
                "flask-cors==5.0.1",
                "flask-RESTful==0.3.10",
                "transformers==4.49.0"]

setuptools.setup(
    name="DeMiCo",
    version="1",
    author="Annemae van de Hoef",
    author_email="annemae.vandehoef@hu.nl",
    description="DeMiCo Prototype Back-end & Front-end",
    url="https://github.com/Annemae/DeMiCo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows 11",
    ],
    install_requires=requirements,
    python_requires='>=3.13.2',
)