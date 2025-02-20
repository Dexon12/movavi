#!/bin/bash

create_and_activate_venv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Virtual environment created."
    else
        echo "Virtual environment already exists."
    fi

    echo "Activating virtual environment..."
    if [[ "$(uname -s)" == *"MINGW"* || "$(uname -s)" == *"CYGWIN"* ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Unix
        source venv/bin/activate
    fi
    echo "Virtual environment activated."
}

install_dependencies() {
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        echo "Dependencies installed."
    else
        echo "Error: requirements.txt not found."
    fi
}

start_without_docker() {
    create_and_activate_venv
    install_dependencies
    py -m app.main
}

while true; do
    clear
    echo "==========================="
    echo "      Check task menu      "
    echo "==========================="
    echo "1) Build and run Docker"
    echo "2) Start task with Docker"
    echo "3) Start task without Docker"
    echo "4) Docker shutdown"
    echo "5) Exit"
    echo "==========================="
    read -p "Enter your choice: " choice


    case "$choice" in
        1)
            echo "Building Docker image..."
            docker build -t app .
            echo $(pwd)

            if [ ! -f "$(pwd -W)/result.json" ]; then
                touch "$(pwd -W)/result.json"
            fi

            echo "Running Docker container in detached mode..."
            docker run -d --name app \
                -v "$(pwd -W):/app" \
                -v "$(pwd -W)/result.json:/result.json" \
                app

            read -p "Docker image built and container started. Press Enter to continue..."
            ;;

        2)
            echo "Starting task with Docker..."
            docker exec -it app python -m app.main
            read -p "Task executed. Press Enter to continue..."
            ;;
        3)
            echo "Starting task without Docker..."
            start_without_docker
            read -p "Task executed. Press Enter to continue..."
            clear
            ;;
        4)
            echo "Shutting down Docker container..."
            docker stop app
            read -p "Container stopped. Press Enter to continue..."
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            read -p "Press Enter to continue..."
            ;;
    esac
done
