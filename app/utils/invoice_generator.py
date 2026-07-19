from datetime import datetime
from uuid import uuid4


class InvoiceGenerator:

    @staticmethod
    def generate() -> str:

        return (
            f"INV-"
            f"{datetime.now():%Y%m%d}-"
            f"{uuid4().hex[:6].upper()}"
        )