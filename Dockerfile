FROM python:3.10-slim

# Install geth
RUN apt-get update && apt-get install -y software-properties-common curl \
    && add-apt-repository -y ppa:ethereum/ethereum \
    && apt-get update && apt-get install -y ethereum \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/gbt

# Copy files
COPY genesis.json /opt/gbt/genesis.json
COPY add_network.html /opt/gbt/add_network.html
COPY app.py /opt/gbt/app.py

# Python deps
RUN pip install fastapi uvicorn httpx

EXPOSE 9636

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9636"]
