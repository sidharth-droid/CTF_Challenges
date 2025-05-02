# Use the official PHP image with Apache
FROM php:8.1-apache

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    && docker-php-ext-install pdo pdo_mysql \
    && a2enmod rewrite

# Set the working directory
WORKDIR /var/www/html

# Copy the challenge files into the container
COPY challenge/ /var/www/html/

# Set permissions for the logs directory (since login.php writes to logs/stats.log)
RUN mkdir -p /var/www/logs && chown -R www-data:www-data /var/www/html /var/www/logs

# Expose port 80 for the web server
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]