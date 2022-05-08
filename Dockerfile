FROM python:3.8
COPY . ./
RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader all
CMD ["Bryson_Module14.py"]
ENTRYPOINT ["python"]