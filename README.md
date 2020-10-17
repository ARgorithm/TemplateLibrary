![](https://byob.yarr.is/ARgorithm/Toolkit/Schema/trial/shields.json) ![Tests](https://github.com/ARgorithm/Toolkit/workflows/Tests/badge.svg)[![PyPI version](https://badge.fury.io/py/ARgorithmToolkit.svg)](https://badge.fury.io/py/ARgorithmToolkit)

# ToolKit
Toolkit Package to use to generate your custom algorithms for AR representation

The package is designed to provide an STL like feature to various data structures and algorithms to support state generation for ARgorithm Unity Application to utilise while rendering an algorithm.

**FOR REFERENCE MANUAL TO USE TOOLKIT** : Check Docs and Examples

<hr/>

### Repository Usage

The repository has a make file for all its major functions :

```bash
$ make init
```
will install all your dependencies

```bash
$ make test
```
Will run tests on code

```bash
$ make verify
```
to verify schemas
```bash
$ make dist
```
will create python dist package for pip. This should only be used when package is up for new release

```bash
$ make testdeploy
```
test deployment of built distribution

```bash
$ make deploy
```
deploy package to PyPip. Required setup of PyPip before that

### Contributing Guidelines

1. **ARgorithmToolkit** is the main package that contains all the functionality for the use case

2. **tests** contains tests created for **ARgorithmToolkit** . These tests are designed for Pytest

3. **schemas** contains schemas for the design each individual data structure

4. make sure to run `make verify` before pushing to ensure schema is up to date with code. This will update `shields.json` , *always push shields.json*

5. Package dependencies that required by **ARgorithmToolkit** should be added in setup.py `install_requires`

   ```python
   install_requires=[
      'A>=1',
      'B>=2'
   ]
   ```

6. Packages needed for environment setup for development should be included in requirements.txt