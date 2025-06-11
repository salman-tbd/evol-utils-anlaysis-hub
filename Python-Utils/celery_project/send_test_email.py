from email_tasks import send_email_task

if __name__ == "__main__":
    result = send_email_task.delay(
        recipient_email="salman.migratezone@gmail.com",  # 👈 replace with your test email
        subject="🎉 Test Email via Celery!",
        html_content="""
            <h2>Hello Salman!</h2>
            <p>This is a test email sent in the background using Celery and Brevo (Sendinblue).</p>
            <p><strong>Nice job setting this up!</strong></p>
        """
    )

    print("Email task sent. Waiting for confirmation...")
    print("Result:", result.get(timeout=30))  # Wait up to 30 seconds for response
