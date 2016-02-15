from setuptools import setup, find_packages

setup(
    name="SensorMesh",
    version="0.0.2.dev1",
    packages=find_packages(),

    install_requires=['requests', 'python-dateutil'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'responses', 'textfixtures'],

    author='James Myatt',
    license="MIT",
    url='https://github.com/Nzbuu/SensorMesh.py',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
