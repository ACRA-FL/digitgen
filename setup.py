from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='digitgen',
    version='0.3.4',
    description='Synthetic Digit Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ACRA-FL/digitgen.git',
    author='DevinDeSilva',
    author_email='devindesilva123@gmail.com',
    packages=['digitgen', 'digitgen/digit', 'digitgen/utils', 'digitgen/augmentation', "digitgen/font"],
    license='MIT',
    python_requires='>=3.8, <4',
    install_requires=['numpy', 'pillow', 'opencv-python','gdown'],
    extras_require={
        'dev': ['check-manifest',
                'pytest>=3.7'],
        'test': ['coverage', 'unittest'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ACRA-FL/digitgen/issues',
        'Source': 'https://github.com/ACRA-FL/digitgen',
    },
)
