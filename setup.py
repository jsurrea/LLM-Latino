from setuptools import setup, find_packages

setup(
    name='seneca_extractor',  # Package name
    version='0.1.0',  # Package version
    packages=find_packages(),  # Automatically find all packages
    description='File and metadata extraction from the Seneca institutional repository of Universidad de los Andes.',  # Short description
    long_description='Extraction of files and metadata from the Seneca institutional repository of Universidad de los Andes for the LLM-Latino project.',  # Long description
    author='David Santiago Ortiz Almanza, Juan Sebastian Urrea Lopez',  # Authors
    author_email='ds.ortiz@uniandes.edu.co, js.urea@uniandes.edu.co',  # Author emails
    install_requires=[
        'pandas',  # Necessary dependencies
        'tqdm',
        'requests'
    ],
    python_requires='>=3.6',  # Minimum required Python version
    url='',  # Project URL (optional, none provided)
    license='MIT',  # License
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development stage of the package
        'Intended Audience :: Developers',  # Target audience
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # License type
        'Programming Language :: Python :: 3',  # Programming language versions
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='seneca, extraction, metadata, repository, Universidad de los Andes, academic, research',  # Keywords
)
