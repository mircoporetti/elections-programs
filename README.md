## Elections Programs AI

### Run the app locally

Requirements:

- Python 3.12
- Poetry

1. Create a `.env` file copied from `.env.example` and fill the `HUGGINGFACEHUB_API_TOKEN` with your HuggingFace personal
Access Token token value.


2. Run

    ```bash
    make run
    ```
    or if you prefer the most annoying way:

    ```bash
    poetry install
    HUGGINGFACEHUB_API_TOKEN=your_token_value poetry run uvicorn src.webapp.main:app --reload
    ```

### Run the tests with

```bash
make test
```