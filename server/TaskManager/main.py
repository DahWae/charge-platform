import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

@app.get('/')
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port = 8001)