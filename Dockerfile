FROM python:3.12
WORKDIR /epg
COPY requirements.txt .
RUN /bin/cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
echo 'Asia/Taipei' > /etc/localtime && \
pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["uwsgi", "uwsgi.dev.ini"]
#CMD ["python", "flask_app.py"]
