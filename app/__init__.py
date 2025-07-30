from fastapi import FastAPI
from app.auth import router as authROuter
from app.user import router as userRouter
from app.mess import router as messRouter
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow requests from your frontend
origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:3001",  # React dev server
    "https://frontend.nuraloom.xyz",
    "http://192.168.0.110:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Or use ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=authROuter,prefix="/auth",tags=["Auth"])
app.include_router(router=userRouter,prefix="/user",tags=["User"])
app.include_router(router=messRouter,prefix="/mess",tags=["Mess"])


@app.get("/")
async def get_root():
    return "Its working"