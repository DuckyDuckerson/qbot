# FROM python:3.12.4
# 
# RUN apt-get update && apt-get install -y \
#     apache2 \
#     libapache2-mod-wsgi-py3 \
#     supervisor \
#     && apt-get clean
# 
# WORKDIR /qbot
# COPY . /qbot
# 
# RUN echo 'DocumentRoot /qbot/public' > /etc/apache2/sites-available/000-default.conf \
#     && echo '<Directory /qbot/public>' >> /etc/apache2/sites-available/000-default.conf \
#     && echo '    Options Indexes FollowSymLinks' >> /etc/apache2/sites-available/000-default.conf \
#     && echo '    AllowOverride All' >> /etc/apache2/sites-available/000-default.conf \
#     && echo '    Require all granted' >> /etc/apache2/sites-available/000-default.conf \
#     && echo '</Directory>' >> /etc/apache2/sites-available/000-default.conf
# 
# EXPOSE 8080 80
# 
# # CMD ["python", "main.py", "apachectl", "-D", "FOREGROUND"]
# 
# # CMD apachectl -D FOREGROUND && python main.py
# 
# # Copy supervisord configuration
# COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# 
# # Use supervisord to run both Apache and the Python bot
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]


FROM python:3.12.4

RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    supervisor \
    && apt-get clean

WORKDIR /qbot
COPY . /qbot

# Copy Cloudflare Origin certificate and private key into the container
COPY origin.pem /etc/ssl/certs/
COPY origin.key /etc/ssl/private/

# Configure Apache to use SSL with the Cloudflare Origin Certificate and Private Key
RUN echo 'Listen 443' >> /etc/apache2/ports.conf \
    && echo '<VirtualHost *:443>' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    ServerName yourdomain.com' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    SSLEngine on' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    SSLCertificateFile /etc/ssl/certs/origin.crt' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    SSLCertificateKeyFile /etc/ssl/private/origin.key' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    SSLCertificateChainFile /etc/ssl/certs/Cloudflare-CA.pem' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    DocumentRoot /qbot/public' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    <Directory /qbot/public>' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '        Options Indexes FollowSymLinks' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '        AllowOverride All' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '        Require all granted' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '    </Directory>' >> /etc/apache2/sites-available/default-ssl.conf \
    && echo '</VirtualHost>' >> /etc/apache2/sites-available/default-ssl.conf

# Enable SSL and the default SSL site configuration
RUN a2enmod ssl \
    && a2ensite default-ssl.conf

# Expose necessary ports
EXPOSE 8080 80 443

# Copy supervisord configuration
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Use supervisord to run both Apache and the Python bot
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

