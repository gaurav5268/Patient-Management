
from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Annotated, Literal, Optional

class Patient(BaseModel):
    id : Annotated[str, Field(..., description = "ID of the patient( example - 001)")]
    name :Annotated[str, Field(..., description = "Name of the patient( example - Guarav Chauhan)")]
    age : Annotated[int, Field(..., gt =0,  lt = 120, description = "Age of the patient( example - 22)")]
    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description = "ID of the patient( example - male)")]
    city : Annotated[str, Field(..., description = "Hometown/Receding city of the patient( example - Varanasi)")]
    height : Annotated[float, Field(..., gt =0,  description = "Height of the patient in cm ( example - 172 cm")]
    weight : Annotated[float, Field(..., gt =0,  description = "Weigth of the patient in kg ( example - 58 kg")]
    status: Annotated[Literal['ongoing', 'over'], Field(..., description="Treatment status")]
    mobile: Annotated[str, Field(..., min_length=10, max_length=10, description="10 digit mobile number")]
    symptoms: Annotated[str, Field(..., description="Selected symptoms (comma separated)")]

    @computed_field
    @property
    def BMI(self) -> float:
        h = self.height / 100
        return round(self.weight / (h ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.BMI < 18.5:
            return "Underweight"
        elif self.BMI < 25:
            return "Normal"
        else:
            return "Overweight"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    status: Optional[Literal['ongoing', 'over']] = None
    mobile: Optional[str] = Field(default=None, min_length=10, max_length=10)
    symptoms: Optional[str] = None

