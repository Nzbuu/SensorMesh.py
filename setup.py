from setuptools import setup, find_packages

setup(
    name="SensorMesh",
    version="0.0.1",
    packages=find_packages(),

    install_requires=['requests', 'python-dateutil'],

    author='James Myatt',
    license="MIT",
    url='https://github.com/Nzbuu/SensorMesh.py',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ]
)
