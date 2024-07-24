FROM python:3.12


COPY . /cars_api
COPY ./pyproject.toml /pyproject.toml

WORKDIR /cars_api
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV INSTALL_DEV=true

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    bash -c "if [ $INSTALL_DEV == 'true' ] ;  \
    then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


