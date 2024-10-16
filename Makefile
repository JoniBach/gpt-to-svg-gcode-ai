.PHONY: start dev build download run clean

start:
	@echo "Starting the FastAPI server..."
	@echo "Visit the server at http://localhost:8000"
	podman run -it --rm -p 8000:8000 my-python-app

dev:
	@echo "Running in development mode..."
	@echo "Visit the server at http://localhost:8000"
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

build:
	@echo "Building Docker image..."
	podman build -t my-python-app .

run:
	@echo "Running the server in container and keeping data..."
	@echo "Visit the server at http://localhost:8000"
	podman run -d -p 8000:8000 -v persistent_storage:/app/static my-python-app

clean:
	@echo "Cleaning up containers, images, and volumes related to my-python-app..."
	# Stop and remove all containers related to the my-python-app image
	-podman ps -a --filter ancestor=my-python-app -q | xargs -r podman stop
	-podman ps -a --filter ancestor=my-python-app -q | xargs -r podman rm
	# Remove the my-python-app image
	-podman images --filter reference='my-python-app' -q | xargs -r podman rmi -f
	# Remove the persistent volume if exists
	-podman volume ls -q --filter name=persistent_storage | xargs -r podman volume rm
