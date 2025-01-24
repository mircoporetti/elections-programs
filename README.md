## Elections Programs AI

### Run the app locally

Requirements:

- Python 3.12
- Poetry

```bash
poetry init
poetry install
poetry run uvicorn src.webapp.main:app --reload
```

### Run the tests with


```bash
poetry run pytest
```