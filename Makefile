.PHONY: start dev build download

start:
	@echo "Starting the FastAPI server..."
	@echo "on http://localhost:8000"
	podman run -it --rm -p 8000:8000 my-python-app

dev:
	@echo "Running in development mode..."
	podman run -it --rm -p 8000:8000 my-python-app uvicorn app:app --reload --host 0.0.0.0 --port 8000

build:
	@echo "Building Docker image..."
	podman build -t my-python-app .

download:
	@echo "Starting the FastAPI server with output files saved to Downloads..."
	@echo "on http://localhost:8000"
	podman run -it --rm -p 8000:8000 -v "C:\Users\jamez\Downloads:/app/static" my-python-app

local:
	@echo "Starting the FastAPI server..."
	@echo "on http://localhost:8000"
	uvicorn app:app --host 0.0.0.0 --port 8000


	