FROM python:3.11-bullseye

RUN pip install tox
COPY . /app
WORKDIR /app
RUN tox run -e app --notest
CMD tox run -e app