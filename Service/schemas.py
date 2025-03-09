from pydantic import BaseModel, model_validator
from typing import Optional

class UserOut(BaseModel):
  Id: str
  FirstName: Optional[str] = None
  LastName: Optional[str] = None
  Email: Optional[str] = None
  EmailVerified: bool = False
  UserRole: Optional[int] = None

  @model_validator(mode="before")
  def set_defaults(cls, values):
      if getattr(values, 'FirstName', None) is None:
          values.FirstName = "Unknown"
      if getattr(values, 'LastName', None) is None:
          values.LastName = "Unknown"
      return values
      
  class Config:
    from_attributes = True
