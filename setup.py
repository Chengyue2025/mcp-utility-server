Here's a `setup.py` file for your `mcp-utility-server` package:

```python
from setuptools import setup, find_packages

setup(
    name='mcp-utility-server',
    version='0.1.0',
    description='MCP server with web_fetch, time, calculator tools',
    author='K3 Unbounded',
    packages=find_packages(),
    install_requires=[
        'fastmcp',
        'requests',
        'pytz',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'mcp-utility-server=mcp_utility_server.main:main',
        ],
    },
)
```

Note: I've assumed you'll have a main module at `mcp_utility_server/main.py` with a `main()` function. If your project structure is different, you'll need to adjust the `entry_points` section accordingly.

You'll also want to create the corresponding package structure:

```
mcp-utility-server/
├── setup.py
├── mcp_utility_server/
│   ├── __init__.py
│   └── main.py
└── README.md (optional)
```

To install the package locally for development, run:
```bash
pip install -e .
```