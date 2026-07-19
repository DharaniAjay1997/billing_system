from reportlab.pdfgen import canvas
from datetime import datetime


class PDFGenerator:

    @staticmethod
    def generate_invoice(bill):

        filename = f"/tmp/{bill.invoice_number}.pdf"
        pdf = canvas.Canvas(filename)

        width, height = pdf._pagesize

        # -----------------------
        # Title
        # -----------------------
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, height - 50, "Invoice Details")

        # -----------------------
        # Invoice Info
        # -----------------------
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, height - 90, bill.invoice_number)

        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, height - 110, f"Email : {bill.customer.email}")

        bill_date = (
            bill.created_at.strftime("%d/%m/%Y, %I:%M:%S %p")
            if hasattr(bill, "created_at")
            else datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")
        )

        pdf.drawString(50, height - 135, f"Date : {bill_date}")

        # -----------------------
        # Table Header
        # -----------------------
        y = height - 180

        headers = [
            ("Product", 50),
            ("Qty", 250),
            ("Price", 310),
            ("Tax %", 380),
            ("Tax", 450),
            ("Total", 530),
        ]

        pdf.setFont("Helvetica-Bold", 11)

        for text, x in headers:
            pdf.drawString(x, y, text)

        y -= 10
        pdf.line(45, y, 570, y)
        y -= 20

        # -----------------------
        # Table Rows
        # -----------------------
        pdf.setFont("Helvetica", 10)

        for item in bill.items:

            pdf.drawString(50, y, item.product.name)
            pdf.drawRightString(270, y, str(item.quantity))
            pdf.drawRightString(350, y, f"{item.unit_price:.2f}")
            pdf.drawRightString(410, y, f"{item.tax_percentage}%")
            pdf.drawRightString(490, y, f"{item.tax_amount:.2f}")
            pdf.drawRightString(570, y, f"{item.line_total:.2f}")

            y -= 20

        # -----------------------
        # Summary
        # -----------------------
        y -= 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Summary")

        y -= 25
        pdf.setFont("Helvetica", 11)

        pdf.drawString(350, y, "Subtotal :")
        pdf.drawRightString(570, y, f"₹{bill.subtotal:.2f}")

        y -= 20
        pdf.drawString(350, y, "Tax :")
        pdf.drawRightString(570, y, f"₹{bill.tax_amount:.2f}")

        y -= 20
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(350, y, "Grand Total :")
        pdf.drawRightString(570, y, f"₹{bill.grand_total:.2f}")

        y -= 20
        pdf.setFont("Helvetica", 11)
        pdf.drawString(350, y, "Cash Paid :")
        pdf.drawRightString(570, y, f"₹{bill.cash_paid:.2f}")

        y -= 20
        pdf.drawString(350, y, "Balance :")
        pdf.drawRightString(570, y, f"₹{bill.balance_amount:.2f}")

        pdf.save()

        return filename