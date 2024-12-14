from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---- Task Schemas ----
class TaskSchema(BaseModel):
    """
    Represent the structure of a task as returned by the API.

    :var id: The unique identifier of the task.
    :type id: int
    :var title: The title of the task.
    :type title: str
    :var description: Additional details about the task.
    :type description: str or None
    :var status: The current status of the task.
    :type status: str
    :var priority: The priority level of the task.
    :type priority: int
    :var due_date: The due date for the task.
    :type due_date: datetime or None
    :var created_at: The creation timestamp of the task.
    :type created_at: datetime
    :var updated_at: The last update timestamp of the task.
    :type updated_at: datetime
    """

    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: int
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Configure Pydantic behavior for the schema.

        :var orm_mode: Enables compatibility with ORM objects.
        :type orm_mode: bool
        :var from_attributes: Allows creating instances from object attributes.
        :type from_attributes: bool
        """
        orm_mode = True
        from_attributes = True


class TaskCreateSchema(BaseModel):
    """
    Represent the data required to create a new task.

    :var title: The title of the task.
    :type title: str
    :var description: Additional details about the task (optional).
    :type description: str or None
    :var status: The initial status of the task (default: "pending").
    :type status: str or None
    :var priority: The priority level of the task (default: 1).
    :type priority: int
    :var due_date: The due date for the task (optional).
    :type due_date: datetime or None
    """

    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: int = 1
    due_date: Optional[datetime] = None


class TaskUpdateSchema(BaseModel):
    """
    Represent the data required to update an existing task.

    All fields are optional, allowing partial updates.

    :var title: The updated title of the task.
    :type title: str or None
    :var description: The updated description of the task.
    :type description: str or None
    :var status: The updated status of the task.
    :type status: str or None
    :var priority: The updated priority level of the task.
    :type priority: int or None
    :var due_date: The updated due date for the task.
    :type due_date: datetime or None
    """

    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[int]
    due_date: Optional[datetime]


# ---- Authentication Schemas ----
class LoginSchema(BaseModel):
    """
    Represent the data required for user login.

    :var username: The username of the user.
    :type username: str
    :var password: The password of the user.
    :type password: str
    """

    username: str
    password: str


class TokenSchema(BaseModel):
    """
    Represent the structure of an authentication token.

    :var token: The authentication token.
    :type token: str
    """

    token: str
