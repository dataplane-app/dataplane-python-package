### Github Actions Release
1. Update release with latest version
2. Github Actions will release to PyPI with that version
3. Automatically update toml and git commit to main
```shell
python update_toml_release.py 0.0.15
```

### Steps to distribute

1. Update toml with latest version

2. In repo root directory build package
```shell
python3 -m pip install --upgrade build
rm -rf ./dist && python3 -m build
```

3. Remove previous version and distribute new package
To use the .pypirc file for authentication, come out of devcontainers
```shell
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```

4. Testing impport times - lazy loading:
```shell
pip install dataplane==0.0.12
python -v import_try.py
```