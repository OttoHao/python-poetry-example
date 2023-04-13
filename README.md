# python-poetry-example

## Init

This repo uses [Poetry](https://python-poetry.org/) to manage dependencies and packaging.

1. Install Poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

2. Configure Credentials for Private Feed

```sh
poetry config http-basic.alchemist-python-shared <username> <PAT>`
```

`username` can be any, `PAT` (Personal Access Token) can be created in Azure.

3. (Optional) Configure In-Project Virtual Environment

By default, Poetry creates a virtual environment in `{cache-dir}/virtualenvs` which is outside of the project.

```sh
poetry config virtualenvs.in-project true
```

4. Install Dependencies and Create Virtual Environment

```sh
poetry install
```

It will help to create virtual environment.

5. Activate the Virtual Environment

```sh
poetry shell
```

6. Set Pre-commit Hooks

```sh
pre-commit install
```