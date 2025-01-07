FROM python:3.12.4

RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    && apt-get clean

WORKDIR /qbot
COPY . /qbot

RUN echo '<Directory /qbot/public>' > /etc/apache2/sites-available/000-default.conf \
    && echo '    Options Indexes FollowSymLinks' >> /etc/apache2/sites-available/000-default.conf \
    && echo '    AllowOverride All' >> /etc/apache2/sites-available/000-default.conf \
    && echo '    Require all granted' >> /etc/apache2/sites-available/000-default.conf \
    && echo '</Directory>' >> /etc/apache2/sites-available/000-default.conf

EXPOSE 8080

# CMD ["python", "main.py", "apachectl", "-D", "FOREGROUND"]

CMD apachetl -D FOREGROUND && python main.py
