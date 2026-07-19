import app.models

from app.core.database import SessionLocal
from app.repositories.billing_repository import BillingRepository
from app.services.email_service import EmailService
from app.task.celery_app import celery
from app.utils.pdf_generator import PDFGenerator

import logging
import os

logger = logging.getLogger(__name__)


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_invoice_email(self, bill_id: int):

    logger.info(f"Task started for bill_id={bill_id}")

    pdf_path = None
    db = SessionLocal()

    try:
        logger.info("Creating repository")

        billing_repository = BillingRepository(db)

        logger.info("Fetching bill")

        bill = billing_repository.get_bill(bill_id)

        logger.info(f"Bill: {bill}")

        pdf_path = PDFGenerator.generate_invoice(bill)

        logger.info(f"PDF: {pdf_path}")

        EmailService.send_email(
            recipient=bill.customer.email,
            subject=f"Invoice {bill.invoice_number}",
            body="Your invoice has been generated.",
            attachment_path=pdf_path,
        )

        logger.info("Email sent successfully")

    except Exception:
        logger.exception("Email task failed")
        raise

    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)

        db.close()