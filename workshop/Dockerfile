FROM python:alpine

ENV POSTGRES_DATABASE=communication

RUN pip install flask
WORKDIR /src
COPY /src .

ENTRYPOINT [ "python3" ]
CMD [ "/src/api.py" ]
