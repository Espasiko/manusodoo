from fastapi import FastAPI
import gc

app = FastAPI(title="Test Minimal Server")

@app.get("/")
async def root():
    # Forzar recolección de basura en cada petición
    gc.collect()
    return {
        "message": "Servidor mínimo funcionando",
        "status": "ok"
    }

@app.get("/health")
async def health():
    gc.collect()
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)