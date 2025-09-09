import subprocess
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

COINBASE = os.getenv("COINBASE", "0xa6a98c491Ede0a953670350d9304dc838B171d1E")

# Initialize chain if not already done
subprocess.run(["geth", "--datadir", "/opt/gbt/data", "init", "/opt/gbt/genesis.json"])

# Start geth node with mining enabled
geth_proc = subprocess.Popen([
    "geth",
    "--datadir", "/opt/gbt/data",
    "--http", "--http.addr", "0.0.0.0", "--http.port", "9635", "--http.api", "eth,net,web3,personal,miner",
    "--networkid", "999",
    "--miner.etherbase", COINBASE,
    "--allow-insecure-unlock",
    "--nodiscover",
    "--mine",
    "--miner.threads", "1"
])

@app.get("/")
async def add_network_page():
    return FileResponse("add_network.html")

@app.post("/")
async def proxy_rpc(req: Request):
    data = await req.body()
    async with httpx.AsyncClient() as client:
        r = await client.post("http://127.0.0.1:9635", content=data, headers={"Content-Type":"application/json"})
        return JSONResponse(r.json())
