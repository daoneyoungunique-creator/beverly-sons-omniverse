FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py api.py dashboard.py checkout.py base44_client.py funnel.py funnel_api.py ./
EXPOSE 8001
CMD ["uvicorn","funnel_api:app","--host","0.0.0.0","--port","8001"]
