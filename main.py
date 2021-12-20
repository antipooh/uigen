from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from models import ModelSection
from transform import class_to_model


class MessageState(Enum):
    NEW = 'new'
    SEND = 'send'
    SEND_ERROR = 'send_error'
    DELIVERED = 'delivered'
    DELIVERY_ERROR = 'delivery_error'


class Message(BaseModel):
    id: Optional[str] = None
    phone: str
    text: str
    planed_at: datetime
    state: MessageState = MessageState.NEW
    state_detail: Optional[str] = None
    ttl: Optional[timedelta] = None
    updated_at: Optional[datetime] = None
    user: Optional[str]
    provider_id: Optional[str] = None
    external_id: Optional[str] = None


print(class_to_model(Message))
# ui = [ModelSection(model=)]
