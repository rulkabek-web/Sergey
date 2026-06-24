from datetime import datetime
from typing  import Optional

from src.main.api.models.base_model import BaseModel

class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: datetime
    #тут в json есть ещё creditId: Bool, в свагере такого поля нет
    
class TransactionsResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transaction]