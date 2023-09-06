# Use the official Python image from the Docker Hub
FROM python:3.11-alpine

# Install system dependencies via alpine package keeper
RUN apk add --no-cache glpk

# Install Python dependencies
RUN pip install pyomo
RUN pip install black pylint

# Set the working directory
WORKDIR /workspace

# Copy the content of the repository into the container
COPY . .