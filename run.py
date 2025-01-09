from app.utils.logger import setup_logger

if __name__ == "__main__":
    setup_logger()  # Initialize logging
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
