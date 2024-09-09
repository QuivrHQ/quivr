# quivr-core package

The RAG of Quivr.com

## Contributors

### Requirements

0. Install [poetry](https://python-poetry.org/docs/). Recommand the `pipx` install
1. (Optional) Install (`uv`)[https://github.com/astral-sh/uv]
2. git clone `quivr`

```
git clone git@github.com:QuivrHQ/quivr.git
cd quivr/backend/core
```

2. Create virtual environement with your preferred tool

   ```
   uv venv
   ```

3. Install `base` quivr-core environment

   ```
   poetry install -E base --with dev,test
   ```

4. Install pre-commit

   ```
   pre-commit install
   ```

5. Run example
   ```
   python examples/simple_question.py
   ```

## Backend

0. Install [poetry](https://python-poetry.org/docs/). Recommand the `pipx` install
1. (Optional) Install (`uv`)[https://github.com/astral-sh/uv]
2. Clone `quivr`

```
cd quivr/backend/
```

2. Create virtual environement with your preferred tool

   ```
   uv venv
   ```

3. Install quivr-core monorepo

   ```
   poetry install
   ```

4. Copy `.env.example` to `.env` and modify env variables : step 2 : (https://docs.quivr.app/install#60-seconds-installation)

5. Run backend-api

```
LOG_LEVEL=debug uvicorn quivr_api.main:app --log-level debug --reload --host 0.0.0.0 --port 5050 --workers 1
```
