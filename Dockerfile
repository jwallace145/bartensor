FROM python:3.8.0

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BARTENSOR_EMAIL_USERNAME bartensor@gmail.com
ENV BARTENSOR_EMAIL_PASSWORD iupeqdduwlekqjrj
ENV WATSON_DISCOVERY_API_KEY Q48Xgoo6dGAAOSNjdUdho8uwprTEbwgXOBUspsEaTDO2
ENV WATSON_SPEECH_TO_TEXT_API_KEY GUyb9Y0-25JUO7_fZtyLvlDipUAMzROb2vxadUiWJEMX

RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/

RUN pip install -U pip
RUN pip install --no-binary pillow pillow

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
