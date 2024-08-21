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
