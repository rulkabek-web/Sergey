from src.main.api.models.base_model import BaseModel

class CreditResponse(BaseModel):
    id: int #в свагере тут "accountId"
    amount: int
    termMonths: int
    balance: int
    creditId: int