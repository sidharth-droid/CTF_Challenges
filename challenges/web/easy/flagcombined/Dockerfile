# Use the official Nginx image as the base
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Copy the challenge files into the container
COPY . /usr/share/nginx/html/

# Expose port 80 for the web server
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]