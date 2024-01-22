from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from xhtml2pdf import pisa

from django.db.models.signals import Signal
from django.dispatch import receiver

invoice_generated = Signal()


def generate_invoice_pdf(customer_email, amount):
    # Render HTML template with dynamic data
    html_content = render_to_string('accounts/invoice.html', {'amount': amount})

    # Generate PDF from HTML
    pdf_file = open("1.pdf", "w+b")
    pisa.CreatePDF(html_content, dest=pdf_file)
    pdf_content = pdf_file.read()
    pdf_file.close()

    return pdf_content

@receiver(invoice_generated)
def handle_invoice_generation(sender, **kwargs):
    customer_email = kwargs['customer_email']
    amount = kwargs['amount']
    pdf_content = generate_invoice_pdf(customer_email, amount)

    # Send email with PDF attachment
    email = EmailMessage(
        'Invoice',
        'Please find attached invoice.',
        'from@example.com',
        [customer_email],
    )
    email.attach('invoice.pdf', pdf_content, 'application/pdf')
    email.send()