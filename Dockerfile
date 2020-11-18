# Derived from official mysql image (our base image)
FROM mysql:latest
# Add a database
ENV MYSQL_DATABASE catvision
ENV MYSQL_ROOT_PASSWORD root
ENV MYSQL_USER catvision
ENV MYSQL_PASSWORD Catvision_1234

WORKDIR /usr/src/app

COPY create_database.sql .

EXPOSE 3306