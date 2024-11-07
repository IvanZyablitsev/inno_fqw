
login:
	docker login ghcr.io

build-push:
	docker buildx build --tag ghcr.io/ivanzyablitsev/inno_fqw/student_predictor:v0.1 --push .
