# Use the official Python 3.9 image from Docker Hub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY app.py /app

# Run app.py when the container starts
CMD ["python", "app.py"]

# -------------------------------
# 📦 BUILD THE IMAGE LOCALLY
# docker build -t my-python-app .

# ▶️ RUN THE CONTAINER LOCALLY
# docker run -p 4000:80 my-python-app

# 🐳 DOCKER HUB
# 🔑 LOGIN TO DOCKER HUB
# docker login

# 🏷️ TAG THE IMAGE FOR DOCKER HUB
# docker tag your_image_name your_dockerhub_username/my-python-app:1.0

# ☁️ PUSH TO DOCKER HUB
# docker push your_dockerhub_username/my-python-app:1.0

# 🧹 REMOVE LOCAL IMAGE (optional)
# docker rmi your_dockerhub_username/my-python-app:1.0

# 🔁 PULL FROM DOCKER HUB AND RUN AGAIN
# docker run your_dockerhub_username/my-python-app:1.0
