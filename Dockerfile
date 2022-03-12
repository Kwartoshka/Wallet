FROM python:3.8
COPY ./ /Wallet
WORKDIR /Wallet
RUN pip install -r requirements.txt
CMD ["python", "Wallet/manage.py", "runserver", "0.0.0.0:8000"]