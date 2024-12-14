from pydantic import BaseModel, validator

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

    @validator("age")
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be at least 18")
        return value



user1 = User(id=1, name="John", email="john@smith.com", age=20)
data = {
    "id": 2,
    "name": "Jane",
    "email": "jane@doe.com",
    "age": 15
}
try:
    user2 = User(**data)
    print("Success")
except ValueError as e:
    print(e)
