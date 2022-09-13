# install requirements
    pip install -r requirements.txt

# Run
    ./run.sh

# Tests
    pytests

# Docker 
    docker build -t to_work_image .
    docker run -d --name to_work_container -p 8000:80 to_work_image

