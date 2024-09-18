# Variables
IMAGE_NAME = bitcoin-flask-app
DOCKER_USERNAME = taimooranwar
DOCKER_PASSWORD = $(DOCKER_PASSWORD)

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run Docker container
run:
	docker run -p 5000:5000 $(IMAGE_NAME)

# Push Docker image to Docker Hub
push:
	echo "$(DOCKER_PASSWORD)" | docker login -u $(DOCKER_USERNAME) --password-stdin
	docker tag $(IMAGE_NAME) $(DOCKER_USERNAME)/$(IMAGE_NAME):latest
	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):latest

# Clean up Docker images
clean:
	docker rmi $(IMAGE_NAME) || true
	docker rmi $(DOCKER_USERNAME)/$(IMAGE_NAME):latest || true
