# DealDirect

![Django](https://img.shields.io/badge/Django-5%2B-brightgreen)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)

![Redis](https://img.shields.io/badge/Redis-Caching-red)

![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Broker-orange)

![Celery](https://img.shields.io/badge/Celery-Queue-green)

![Pytest](https://img.shields.io/badge/Pytest-Testing-yellow)

![Docker](https://img.shields.io/badge/Docker-Ready-blue)

![SQLite](https://img.shields.io/badge/SQLite-Development-lightgrey)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue)

![License](https://img.shields.io/badge/License-MIT-yellow)

***------------------------------------------------***
## Table of Contents
- [Endpoints](#endpoints)
- [ERD](#erd)
- [Code Formatting](#code-formatting)
  - [Pre-commit Hooks](#pre-commit-hooks)
- [Usage](#usage)
- [Testing](#testing)

***------------------------------------------------***
## Endpoints

To see the current endpoints, run the following command:

```bash
python manage.py stdout_endpoints > ENDPOINTS.md
```
***------------------------------------------------***
## ERD
checkout the diagram at:

- [ERD](documents/Entity%20Relationship%20Diagram.jpg)


***------------------------------------------------***
## Code Formatting

This project uses `black` for code formatting. Black is a code formatter for Python that ensures consistent code style.

### Pre-commit Hooks
Pre-commit hooks are used to ensure code quality before committing changes. This project uses the following pre-commit hooks:

- check-yaml: Checks YAML files for syntax errors.


- end-of-file-fixer: Ensures files end with a newline.


- trailing-whitespace: Removes trailing whitespace.


- black: Formats Python code using black.

To install the pre-commit hooks, run:

```bash
pre-commit install
```
to run the pre-commit hooks manually, use:
```bash
pre-commit run --all-files
```

***------------------------------------------------***
## Usage

1. Clone the repository:
```bash
git clone git@github.com:serene1212/porsojo.git
```
2. Navigate to the project directory:

```bash
cd deal_direct
```
3. Install the required packages:

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```
4. Copy sample.env and change variables:

```bash
cp sample.env .env
```
5. Run the server:

```bash
python manage.py runserver
```

***------------------------------------------------***

## Testing
This project aims to achieve over 95% test coverage.

All tests are written using **`pytest`**.

To run the tests and see the coverage report, use the following command:

```bash
pytest --cov --cov-config=.coveragerc
```

**this command will exclude **`custom_commands`** directory from testing**
