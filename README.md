# Text2SQL

<!--
.. image:: https://img.shields.io/pypi/v/text2sql.svg
        :target: https://pypi.python.org/pypi/text2sql

.. image:: https://img.shields.io/travis/soluds/text2sql.svg
        :target: https://travis-ci.com/soluds/text2sql

.. image:: https://readthedocs.org/projects/text2sql/badge/?version=latest
        :target: https://text2sql.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status -->

Prends des requetes en langage naturel et les transforme en requete SQL.



* Free software: MIT license
* Documentation: [https://lxre0981pv.res.private:4083/documentation/text2sql/](<https://lxre0981pv.res.private:4083/documentation/text2sql/>).


## Getting started

### install package

you should install the package text2sql with the following command:

```bash
pip install text2sql --default-timeout=1000 --extra-index-url https://bdistrib-build.sofact.banque-france.fr/artifactory/api/pypi/bdf-siad-python/simple
```

## Documentation

You can access the documentation [here](<https://lxre0981pv.res.private:4083/documentation/text2sql/>) and the sources are [there](<https://scm.sofact.banque-france.fr/soluds/text2sql>).

## Developpers

### install the source code

To install the source code, you should clone this repository and install it with the following commands:

```bash
git clone https://scm.sofact.banque-france.fr/soluds/text2sql.git
cd git clone
python -m venv env
source env/bin/activate
pip install --default-timeout=1000 -r requirements.txt -r requirements-dev.txt
pip install -e .
```

You're all set to go !

### use pre-commit hook (so your commits are always nice :)

1. If not done, install the requirements for developpers `pip install requirements-dev.txt`.

1. At the root of the project, modify the file `.pre-commit-config.yaml` if necessary.

1. At the root of the project, to run manually the pre-commit hooks manually (recommended after the previous step to check that everything works), run `pre-commit run --all-files`.

1. At the root of the project, to run automatically before every commits, run `pre-commit install`.

### run tests

to run the tests, you should run the following command:

```bash
pytest tests
```

### update the documentation

to create the documentation, you should run the following command in the documentation folder:

```bash
make clean && make html
```

## Features

* TODO

## Credits

This package was created with Cookiecutter<sup>[1]</sup> and the `soluds/cookiecutter-iliade`<sup>[2]</sup> project template.

[1]: [cookiecutter](https://github.com/cookiecutter/cookiecutter)
[2]: [`soluds/cookiecutter-iliade`](https://scm.sofact.banque-france.fr/soluds/cookiecutter-iliade)
