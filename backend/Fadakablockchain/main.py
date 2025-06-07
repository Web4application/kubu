from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
import time

app = FastAPI(title="Kubu-Hai AI-Blockchain API")

# === Configs & Secrets ===
JWT_SECRET = "supersecretkey"  # Replace with env var in prod
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # 1 hour


# === Auth Models & Utils ===

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    username: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    expire = time.time() + (expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return User(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)


# === Auth Endpoint ===

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Dummy auth — replace with your real user validation
    if form_data.username == "kubu" and form_data.password == "lee123":
        access_token = create_access_token(data={"sub": form_data.username})
        return Token(access_token=access_token)
    raise HTTPException(status_code=400, detail="Incorrect username or password")


# === AI Inference Stub ===

class AIRequest(BaseModel):
    prompt: str

class AIResponse(BaseModel):
    response: str

@app.post("/ai/infer", response_model=AIResponse)
async def ai_infer(request: AIRequest, user: User = Depends(get_current_user)):
    # Dummy response; plug your AI inference logic here
    text = request.prompt
    generated = f"Echo from AI model: {text[::-1]}"  # Just reverse input as a placeholder
    return AIResponse(response=generated)


# === Blockchain Interaction Stub ===

class BlockchainTx(BaseModel):
    to_address: str
    amount: float
    data: Optional[str] = None

class BlockchainResponse(BaseModel):
    tx_hash: str
    status: str

@app.post("/blockchain/send", response_model=BlockchainResponse)
async def send_tx(tx: BlockchainTx, user: User = Depends(get_current_user)):
    # Dummy blockchain tx — replace with your real blockchain call
    tx_hash = "0xdeadbeef1234567890"
    return BlockchainResponse(tx_hash=tx_hash, status="submitted")


# === Health Check ===
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "kubu-hai AI-Blockchain API"}

