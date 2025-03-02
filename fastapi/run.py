import uvicorn
from app.wsgi import app
   
if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=5000, reload=False)
    