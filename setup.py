from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# The runtime requirements
RUNTIME_PACKAGES = [
    'hidapi',
    'colour'
]

# Additional requirements used during setup
SETUP_PACKAGES = []

# Packages required for different environments
EXTRA_PACKAGES = {}

setup(
    name='py_wraith_prism',
    version='0.9.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=RUNTIME_PACKAGES,
    setup_requires=RUNTIME_PACKAGES + SETUP_PACKAGES,
    extras_require=EXTRA_PACKAGES,
    url='https://github.com/dfraska/PyWraithPrism/',
    license='MIT',
    author='David Fraska',
    author_email='dfraska@gmail.com',
    description='Control the Wraith Prism CPU fan LEDs from Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='Wraith Prism, LEDs, LED',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: POSIX',
    ]
)
