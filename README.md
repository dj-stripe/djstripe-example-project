# djstripe Example Project

This repository is an example project for the `dj-stripe` Django app. It's designed to help developers understand how to integrate and use `dj-stripe` in a Django project by providing a basic setup.

## Requirements

- Python 3.9+
- Django 4.2+
- Poetry

## Setup

1. **Clone the repository:**
   Use the command `git clone https://github.com/dj-stripe/dj-stripe-example-project.git` and then enter the project directory with `cd dj-stripe-example-project`.

2. **Install dependencies with Poetry:**
   Depending on your setup, you can install `dj-stripe` in one of two ways:
   - From the GitHub master branch: `poetry add dj-stripe`
   - From a local directory, assuming `dj-stripe` is in a sibling directory: Update the `pyproject.toml` to include `dj-stripe = { path = "../dj-stripe" }` and then run `poetry install`.

```
parent_directory/
│
├── dj-stripe/            # dj-stripe library repository
│
└── djstripe-example-project/  # djstripe example project repository
```

3. **Create a `.env` file:**
   Copy the `.env.dist` file to `.env` and fill in the required values.

4. **Run migrations:**
   Initialize your database by executing `poetry run python manage.py migrate`.

5. **Start the development server:**
   Launch the server with `poetry run python manage.py runserver`.

## Contributing

Contributions to both the example project and the `dj-stripe` main library are welcome. Please refer to the main repository at [dj-stripe](https://github.com/dj-stripe/dj-stripe) for more details.

## License

This project is released under the MIT License. For more details, refer to the `LICENSE` file.
