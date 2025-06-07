from celery import Celery

celery_app = Celery('tasks', broker=os.getenv('REDIS_URL'))

@celery_app.task
def async_blockchain_send(tx_data):
    # Your blockchain send logic here
    pass

@app.post("/blockchain/send-async")
async def send_tx_async(tx: BlockchainTx, user: User = Depends(get_current_user)):
    task = async_blockchain_send.delay(tx.dict())
    return {"task_id": task.id, "status": "queued"}
