<p align="center">
    <img alt="kitconcept GmbH" width="200px" src="https://kitconcept.com/logo.svg">
</p>

<h1 align="center">collective.blog</h1>
<h3 align="center">Blog features for Plone</h3>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.blog)](https://pypi.org/project/collective.blog/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.blog)](https://pypi.org/project/collective.blog/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.blog)](https://pypi.org/project/collective.blog/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.blog)](https://pypi.org/project/collective.blog/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.blog)](https://pypi.org/project/collective.blog/)

[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.blog)](https://pypi.org/project/collective.blog/)

[![Meta](https://github.com/collective/collective.blog/actions/workflows/meta.yml/badge.svg)](https://github.com/collective/collective.blog/actions/workflows/meta.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.blog)](https://github.com/collective/collective.blog)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.blog?style=social)](https://github.com/collective/collective.blog)

</div>

## Features

`collective.blog` adds blogging features to a [Plone](https://plone.org/) site.

### Content Types

| name    | context                         |
| ------- | ------------------------------- |
| `Blog` | A folderish content type that supports adding Posts and Authors |
| `Blog Author` | An Author in a blog |
| `Blog Post` | A Post in a blog |


Installation
------------

Add `collective.blog` as a dependency on your package's `setup.py`

```python
    install_requires = [
        "collective.blog",
        "Plone",
        "plone.restapi",
        "setuptools",
    ],
```

Also, add `collective.blog` to your package's `configure.zcml` (or `dependencies.zcml`):

```xml
<include package="collective.blog" />
```

### Generic Setup

To automatically enable this package when your add-on is installed, add the following line inside the package's `profiles/default/metadata.xml` `dependencies` element:

```xml
    <dependency>profile-collective.blog:default</dependency>
```

## Source Code and Contributions

We welcome contributions to `collective.blog`.

You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/collective/collective.blog/issues)
- [Source Code](https://github.com/collective/collective.blog/)

### Development requirements

- Python 3.8 or later
- Docker

### Setup

Install all development dependencies -- including Plone -- and create a new instance using:

```bash
make install
```

### Update translations

```bash
make i18n
```

### Format codebase

```bash
make format
```

### Run tests

Testing of this package is done with [`pytest`](https://docs.pytest.org/) and [`tox`](https://tox.wiki/).

Run all tests with:

```bash
make test
```

Run all tests but stop on the first error and open a `pdb` session:

```bash
./bin/tox -e test -- -x --pdb
```

Run only tests that match `TestVocabAuthors`:

```bash
./bin/tox -e test -- -k TestVocabAuthors
```

Run only tests that match `TestVocabAuthors`, but stop on the first error and open a `pdb` session:

```bash
./bin/tox -e test -- -k TestVocabAuthors -x --pdb
```

## Credits

The development of this add-on has been kindly sponsored by [German Aerospace Center (DLR)](https://www.dlr.de) and [Forschungszentrum Jülich](https://www.fz-juelich.de).

<img alt="German Aerospace Center (DLR)" width="200px" src="https://raw.githubusercontent.com/collective/collective.blog/main/docs/dlr.svg" style="background-color:white">
<img alt="Forschungszentrum Jülich" width="200px" src="https://raw.githubusercontent.com/collective/collective.blog/main/docs/fz-juelich.svg" style="background-color:white">

Developed by [kitconcept](https://www.kitconcept.com/)

## License

The project is licensed under GPLv2.
