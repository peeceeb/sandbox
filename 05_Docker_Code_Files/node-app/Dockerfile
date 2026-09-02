# Start with Node.js on Alpine Linux, a small Linux distribution suited to containers.
FROM node:20.17.0-alpine3.19

# All following commands run inside this directory in the image.
WORKDIR /home/app/

# Copy package files first so Docker can reuse the dependency layer when source code changes.
COPY package*.json .
# Install the dependencies declared in package.json.
RUN npm install

# Copy the application entry point into the image.
COPY index.js index.js

# Keep a copy of the Dockerfile in the image for demonstration and inspection.
COPY Dockerfile Dockerfile

# Configure the port used by index.js and document it for Docker tooling.
ENV PORT=8000
EXPOSE 8000

# Start the application when a container is created from this image.
CMD [ "npm", "start" ]
