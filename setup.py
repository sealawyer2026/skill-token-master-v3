#!/usr/bin/env python3
"""
Setup script for Token经济大师 v3.3.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / 'README.md'
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ''

setup(
    name='token-economy-master',
    version='3.3.0',
    author='白泽',
    author_email='',
    description='Token经济大师 - 智能Token优化工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sealawyer2026/skill-token-master-v3',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    install_requires=[
        'sqlparse>=0.4.0',
    ],
    entry_points={
        'console_scripts': [
            'token-master=cli.token_master_cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
