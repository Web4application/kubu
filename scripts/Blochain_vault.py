from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import hvac
import os

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

vault_client = hvac.Client(url=os.getenv("VAULT_ADDR"))
vault_client.token = os.getenv("VAULT_TOKEN")
secret = vault_client.secrets.kv.v2.read_secret_version(path="kubu/blockchain")
BLOCKCHAIN_PRIVATE_KEY = secret['data']['data']['private_key']

def verify_token(token: str = Depends(oauth2_scheme)):
    # Add your JWT validation here
    if token != "valid-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

@app.get("/blockchain/private-key")
def get_private_key(token: str = Depends(verify_token)):
    return {"private_key": BLOCKCHAIN_PRIVATE_KEY[:5] + "...hidden..."}
