# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9

WORKDIR /UI

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python","app.py"]
