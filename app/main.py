from fastapi import FastAPI,status,APIRouter,Depends


app=FastAPI()



@app.get("/healthy",status_code=status.HTTP_200_OK)
def check_server():
    return {
        "status" :"Server is Healthy",
        "success":True
    }