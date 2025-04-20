docker.build:
	docker build --no-cache -t jpeg2000-reader:latest .

docker.run:
	docker run -it --rm jpeg2000-reader:latest --help

docker.run.tests:
	docker run -v "$(PWD)/tests/assets:/assets" -it --rm jpeg2000-reader:latest /assets/black_2k.j2c
