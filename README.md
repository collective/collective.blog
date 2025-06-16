<div align="center">
<picture>
  <source width="200" media="(prefers-color-scheme: dark)" srcset="https://kitconcept.com/kitconcept-white.svg">
  <img width="200" alt="kitconcept, GmbH" src="https://kitconcept.com/kitconcept-black.svg">
</picture>

<h1 align="center">collective.blog</h1>
<h3 align="center">Blog features for Plone</h3>

[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookieplone-0083be.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![CI](https://github.com/collective/collective.blog/actions/workflows/ci.yml/badge.svg)](https://github.com/collective/collective.blog/actions/workflows/ci.yml)

</div>

> [!WARNING]
> This add-on is meant to be used in combination with the [volto-light-theme](https://github.com/kitconcept/volto-light-theme). If you plan to use this add-on with plain Volto you will have to write your own styles for it. You can use the existing ones via manual import in your config file like this `import "@kitconcept/volto-carousel/theme/_main.scss"` or as reference.

> [!WARNING]
> This add-on customizes the `vocabularies` and `querystring` actions to ensure tags and authors are scoped per blog. Since multiple blogs are supported, these actions now retrieve data based on the current context. This change is marked as breaking in Volto. If you have customited other components relying on these actions, it may cause compatibility issues.

## Features

`collective.blog` adds blogging features to a [Plone](https://plone.org/) site.

### Content Types

| name          | context                                                         |
| ------------- | --------------------------------------------------------------- |
| `Blog`        | A folderish content type that supports adding Posts and Authors |
| `Blog Author` | An Author in a blog                                             |
| `Blog Tag`    | A Tag for categorizing posts in a blog                          |
| `Blog Post`   | A Post in a blog                                                |

## Installation

### Backend

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

#### Generic Setup

To automatically enable this package when your add-on is installed, add the following line inside the package's `profiles/default/metadata.xml` `dependencies` element:

```xml
<dependency>profile-collective.blog:default</dependency>
```

### Frontend

To install your project, you must choose the method appropriate to your version of Volto.

#### Volto 18 and later

Add `@plone-collective/volto-blog` to your `package.json`:

```json
"dependencies": {
    "@plone-collective/volto-blog": "*"
}
```

Add `@plone-collective/volto-blog` to your `volto.config.js`:

```javascript
const addons = ['@plone-collective/volto-blog'];
```


#### Volto 17 and earlier

Add `@plone-collective/volto-blog` to your package.json:

```json
"addons": [
    "@plone-collective/volto-blog"
],
```

## Source Code and Contributions 🏁

We welcome contributions to `collective.blog`.

You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/collective/collective.blog/issues)
- [Source Code](https://github.com/collective/collective.blog/)

### Development requirements ✅

Ensure you have the following installed:

- Python 3.12 or later 🐍
- uv 🚀
- Node 22 🟩
- pnpm 🧶

### Setup 🔧

1. Clone the repository:

```shell
git clone git@github.com:collective/collective.blog.git
cd collective.blog
```

2. Install both Backend and Frontend:

```shell
make install
```

### Fire Up the Servers 🔥

1. Create a new Plone site on your first run:

```shell
make backend-create-site
```

2. Start the Backend at [http://localhost:8080/](http://localhost:8080/):

```shell
make backend-start
```

3. In a new terminal, start the Frontend at [http://localhost:3000/](http://localhost:3000/):

```shell
make frontend-start
```

Voila! Your Plone site should be live and kicking! 🎉

## Project Structure 🏗️

This monorepo consists of the following distinct sections:

- **backend**: Houses the API and Plone installation, utilizing uv instead of buildout, and includes a policy package named collective.blog.
- **frontend**: Contains the React (Volto) package.
- **devops**: Encompasses Docker Stack, Ansible playbooks, and Cache settings.
- **docs**: Scaffold for writing documentation for your project.

### Why This Structure? 🤔

- All necessary codebases to run the site are contained within the repo (excluding existing addons for Plone and React).
- Specific GitHub Workflows are triggered based on changes in each codebase (refer to .github/workflows).
- Simplifies the creation of Docker images for each codebase.
- Demonstrates Plone installation/setup without buildout.

## Code Quality Assurance 🧐

To automatically format your code and ensure it adheres to quality standards, execute:

```shell
make check
```

### Format the codebase

To format the codebase, it is possible to run `format`:

```shell
make format
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Python code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | `zpretty` | XML and ZCML formatting  | -- |
| frontend | ESLint | Fixes most common frontend issues | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Format JS and Typescript code  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Format Styles (css, less, sass)  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Formatters can also be run within the `backend` or `frontend` folders.

### Linting the codebase
or `lint`:

 ```shell
make lint
```

| Section | Tool | Description | Configuration |
| --- | --- | --- | --- |
| backend | Ruff | Checks code formatting, imports sorting  | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | Pyroma | Checks Python package metadata  | -- |
| backend | check-python-versions | Checks Python version information  | -- |
| backend | `zpretty` | Checks XML and ZCML formatting  | -- |
| frontend | ESLint | Checks JS / Typescript lint | [`frontend/.eslintrc.js`](.frontend/.eslintrc.js) |
| frontend | prettier | Check JS / Typescript formatting  | [`frontend/.prettierrc`](.frontend/.prettierrc) |
| frontend | Stylelint | Check Styles (css, less, sass) formatting  | [`frontend/.stylelintrc`](.frontend/.stylelintrc) |

Linters can be run individually within the `backend` or `frontend` folders.

## Internationalization 🌐

Generate translation files for Plone and Volto with ease:

```shell
make i18n
```

## Credits and Acknowledgements 🙏

The development of this add-on has been kindly sponsored by [German Aerospace Center (DLR)](https://www.dlr.de) and [Forschungszentrum Jülich](https://www.fz-juelich.de).

<img alt="German Aerospace Center (DLR)" width="200px" src="https://raw.githubusercontent.com/collective/collective.blog/main/docs/docs/_static/dlr.svg" style="background-color:white">
<img alt="Forschungszentrum Jülich" width="200px" src="https://raw.githubusercontent.com/collective/collective.blog/main/docs/docs/_static/fz-juelich.svg" style="background-color:white">

Made with ❤️ by [kitconcept](https://www.kitconcept.com/)

## License

The project is licensed under GPLv2.
