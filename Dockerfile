FROM python:3.11

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "Docker/streamlit.py", "--server.port=8080", "--server.address=0.0.0.0"]
