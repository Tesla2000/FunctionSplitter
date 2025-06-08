## Running

You can run script with docker or python

### Python
```shell
python main.py --config_file function_splitter/config_sample.toml
```

### Cmd
```shell
poetry install
poetry run function_splitter
```

### Docker
```shell
docker build -t FunctionSplitter .
docker run -it FunctionSplitter /bin/sh
python main.py
```
