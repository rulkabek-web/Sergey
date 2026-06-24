from datetime import datetime
from typing import Optional

from src.main.api.models.base_model import BaseModel


class Credits(BaseModel):
    creditId: int
    accountId: int
    amount: float
    termMonths: int
    balance: float
    createdAt: datetime

class CreditHistoryResponse(BaseModel):
    userId: int
    credits: list[Credits]