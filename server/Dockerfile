FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple anomaly-det-model

COPY . /app

EXPOSE 8061

CMD ["python", "./server_main.py"]