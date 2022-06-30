import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="bakeneko.web:app", port=5000, log_level="debug", reload=True)
