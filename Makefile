.EXPORT_ALL_VARIABLES:
__POETRY_FLAGS = 
POETRY_FLAGS = 
include .env
POETRY_FLAGS += $(__POETRY_FLAGS)
SRC_FILES := $(shell find src -type f)
env:
	env
	env | grep POETRY
tests/tmp:
	mkdir -p tests/tmp
poetry.lock: pyproject.toml
	poetry check
	poetry install --no-interaction --no-ansi $(POETRY_FLAGS)
	# poetry update
build-packages: poetry.lock $(SRC_FILES)
	poetry build

dist/pbivcs: $(SRC_FILES)
	poetry run pyinstaller --noconfirm --clean --distpath=dist $(SPEC_FILE)
build-bin: export PYTHONHASHSEED = 1
build-bin: build-packages dist/pbivcs
	cksum dist/pbivcs | awk '{print $1}' > dist/pbivcs.txt
# TODO: move to tests
test-00: tests/tmp dist/pbivcs
	# ./tests/xc.sh
	./dist/pbivcs --version
	./dist/pbivcs --overwrite --extract "./samples/IT Spend Analysis Sample PBIX.pbit" "./tests/tmp/IT Spend Analysis Sample PBIX"
	./dist/pbivcs --overwrite --compress "./tests/tmp/IT Spend Analysis Sample PBIX" "./tests/tmp/IT Spend Analysis Sample PBIX.pbit"
docker-build:
	docker-compose up --build
.PHONY: clean
clean:
	rm -r build dist logs tests/tmp *.ses
	py3clean .
	# find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +
tox:
	 poetry run tox
