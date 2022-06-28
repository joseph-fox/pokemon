# Pull official base image
FROM python:3.9.7-slim-buster

# Set work directory
WORKDIR /usr/src/app


# Install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock

# Expose port
EXPOSE 5090

# Install python dependencies
RUN set -ex; \
  \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    jq \
    build-essential \
    netcat \
    telnet \
    procps \
    libgnutls28-dev \
    libgdal-dev \
    libmemcached-dev;\
	rm -rf /var/lib/apt/lists/*; \
	pip install pip -U; \
	pip install pipenv && pipenv install --dev --system

# Set work directory
WORKDIR /usr/src/app/src

# Copy application
COPY . /usr/src/app/

ENTRYPOINT ["../docker/entrypoint.sh"]
