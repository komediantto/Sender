FROM python:3.10

WORKDIR /app/
RUN apt update
RUN apt install -y python3-pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock* /app/
# RUN poetry add flask-login
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"
COPY . /app
ENV PYTHONPATH=/app
