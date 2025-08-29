from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    name: str
    age: int
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        from_attributes = True   # Pydantic v2