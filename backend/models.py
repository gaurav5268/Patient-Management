from pydantic import BaseModel
from typing import Optional, List

class Patient(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    city: str
    height: float
    weight: float
    status: str
    mobile: str
    symptoms: List[str]


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    status: Optional[str] = None
    mobile: Optional[str] = None
    symptoms: Optional[List[str]] = None

