
login:
	docker login ghcr.io -u IvanZyablitsev

build-push:
	docker buildx build --tag ghcr.io/ivanzyablitsev/inno_fqw/gradio_app:v0.1 --push .
