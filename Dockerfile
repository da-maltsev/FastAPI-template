FROM python:3.10

EXPOSE 8000

WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3
ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* /app/
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY . .

ARG START_LOCAL=${START_LOCAL}
ARG HOST=${HOST}
ARG PORT=${PORT}

CMD sh start.sh