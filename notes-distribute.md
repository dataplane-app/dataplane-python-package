### Steps to distribute

In repo root directory build package
```shell
python3 -m pip install --upgrade build
python3 -m build
```

Distribute package
```shell
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```