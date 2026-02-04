from fastapi import FastAPI

app = FastAPI(title="PaideraCont")

@app.get("/")
def root():
    return {"status": "PaideraCont rodando 🚀"}
