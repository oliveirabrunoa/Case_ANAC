FROM python:3.10

WORKDIR /case-anac

COPY requeriments.txt  requeriments.txt
RUN pip install -r requeriments.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]