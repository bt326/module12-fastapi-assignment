from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide
import uvicorn
import logging
from app.database import Base, engine, SessionLocal
from app.models import User, Calculation
from app.schemas import (
    UserCreate,
    UserRead,
    UserLogin,
    CalculationCreate,
    CalculationRead
)
from app.security import hash_password, verify_password
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    result: float


class ErrorResponse(BaseModel):
    error: str


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join(
        [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    )
    return JSONResponse(
        status_code=400,
        content={"error": error_messages},
    )


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- Calculator Routes ----------------

@app.post("/add", response_model=OperationResponse)
async def add_route(operation: OperationRequest):
    return {"result": add(operation.a, operation.b)}


@app.post("/subtract", response_model=OperationResponse)
async def subtract_route(operation: OperationRequest):
    return {"result": subtract(operation.a, operation.b)}


@app.post("/multiply", response_model=OperationResponse)
async def multiply_route(operation: OperationRequest):
    return {"result": multiply(operation.a, operation.b)}


@app.post("/divide", response_model=OperationResponse)
async def divide_route(operation: OperationRequest):
    try:
        return {"result": divide(operation.a, operation.b)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero!")


# ---------------- User Routes ----------------

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


@app.post("/users/register", response_model=UserRead)
def register_user(user: UserCreate):
    return create_user(user)


@app.post("/users/login")
def login_user(user: UserLogin):
    db: Session = SessionLocal()

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db.close()
    return {"message": "Login successful"}


# ---------------- Calculation CRUD ----------------

def calculate_result(operation: str, a: float, b: float):
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero!")
        return a / b
    else:
        raise HTTPException(status_code=400, detail="Invalid operation")


@app.post("/calculations", response_model=CalculationRead)
def create_calculation(data: CalculationCreate):
    db: Session = SessionLocal()
    result = calculate_result(data.operation, data.a, data.b)

    calc = Calculation(
        operation=data.operation,
        a=data.a,
        b=data.b,
        result=result
    )

    db.add(calc)
    db.commit()
    db.refresh(calc)
    db.close()
    return calc


@app.get("/calculations", response_model=list[CalculationRead])
def get_calculations():
    db: Session = SessionLocal()
    data = db.query(Calculation).all()
    db.close()
    return data


@app.get("/calculations/{calc_id}", response_model=CalculationRead)
def get_calculation(calc_id: int):
    db: Session = SessionLocal()
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    db.close()

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    return calc


@app.put("/calculations/{calc_id}", response_model=CalculationRead)
def update_calculation(calc_id: int, data: CalculationCreate):
    db: Session = SessionLocal()
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()

    if not calc:
        db.close()
        raise HTTPException(status_code=404, detail="Calculation not found")

    calc.operation = data.operation
    calc.a = data.a
    calc.b = data.b
    calc.result = calculate_result(data.operation, data.a, data.b)

    db.commit()
    db.refresh(calc)
    db.close()
    return calc


@app.delete("/calculations/{calc_id}")
def delete_calculation(calc_id: int):
    db: Session = SessionLocal()
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()

    if not calc:
        db.close()
        raise HTTPException(status_code=404, detail="Calculation not found")

    db.delete(calc)
    db.commit()
    db.close()

    return {"message": "Calculation deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)