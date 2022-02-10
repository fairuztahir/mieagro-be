# Requirement (test in local machine w/out docker)

Need to install all required libs in requirements.txt
and run below commands

```sh
pip install sanic-testing
pip install pytest-asyncio
```

# 3 type of mode:

auto, strict, legacy (default)

# To run sanic test:

```sh
$ pytest folder-name --asyncio-mode=auto
```

# Example from root folder:

```sh
$ cd sanicbe/
$ pytest src/tests --asyncio-mode=auto
```

# Requirement (to test using docker)

From `docker/` folder path, run command below

```sh
$ cd docker/
$ make test
```

to stop the test app

```sh
$ make test-destroy
```
