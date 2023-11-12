from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models.models
from db.database import engine
from routes import auth, todos

app = FastAPI()

# Add middleware to allow all origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

models.models.Base.metadata.create_all(bind=engine)

# Right here we connect our routes with our main application
app.include_router(auth.route)
app.include_router(todos.route)

