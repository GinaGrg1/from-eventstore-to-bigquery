FROM python:3.6-alpine3.6
ENV TERM=xterm

COPY requirements.txt /tmp/requirements.txt

RUN apk --update upgrade && \
    apk add bash libpq python3-dev linux-headers postgresql-dev ncurses-dev build-base && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    apk del bash python3-dev postgresql-dev ncurses-dev linux-headers build-base && \
    rm -rf /var/cache/apk/*


COPY ./src /code/src
COPY entrypoint.sh /bin/entrypoint

CMD ["/bin/entrypoint"]