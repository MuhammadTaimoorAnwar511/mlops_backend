# Define variables
IMAGE_NAME=yourdockerhubusername/bitcoin-predictor:latest

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Push the Docker image to Docker Hub
push:
	docker push $(IMAGE_NAME)

# Run the Docker container
run:
	docker run -p 5000:5000 $(IMAGE_NAME)

# Stop the container (example if using container name or ID)
stop:
	docker stop $(docker ps -q --filter ancestor=$(IMAGE_NAME))
