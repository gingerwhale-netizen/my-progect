from src.main.api.models.base_model import BaseModel



class CreditResponse(BaseModel):
    id: int  # серверный ключ "id"; по документации это accountId
    amount: float
    termMonths: int
    balance: float
    creditId: int
