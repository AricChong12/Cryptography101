FROM python:3.11-slim AS app
RUN pip install --no-cache-dir pycryptodome
RUN apt-get update && apt-get install -y dos2unix 
FROM pwn.red/jail
COPY --from=app / /srv
COPY server.py /srv/app/run
RUN chmod +x /srv/app/run
COPY quotes.py /srv/app/quotes.py
RUN dos2unix /srv/app/run
ENV JAIL_MEM=20M JAIL_ENV_NUM=5