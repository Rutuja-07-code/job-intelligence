from fastapi import FastAPI

from .routers import companies, jobs, users

app = FastAPI()

app.include_router(companies.router)
app.include_router(jobs.router)
app.include_router(users.router)