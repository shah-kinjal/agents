def process_emails_with_message(email_list, message):
    """
    Loops through a list of email addresses and processes them with an additional message.
    
    Args:
        email_list (list): List of email addresses to process
        message (str): Additional string message to include with each email
    
    Returns:
        dict: Dictionary with processed email information
    """
    results = {}
    
    for email in email_list:
        # Basic email validation
        if "@" in email and "." in email.split("@")[1]:
            # Extract domain from email
            domain = email.split("@")[1]
            
            # Process the email with the additional message
            processed_info = {
                'email': email,
                'domain': domain,
                'message': message,
                'status': 'valid',
                'processed_at': f"2024-01-01 12:00:00"  # In real app, use datetime.now()
            }
            
            results[email] = processed_info
            print(f"✓ Processed {email} from {domain} - Message: {message}")
        else:
            results[email] = {
                'email': email,
                'message': message,
                'status': 'invalid',
                'error': 'Invalid email format'
            }
            print(f"✗ Invalid email format: {email}")
    
    return results


def send_newsletter_emails(subscriber_emails, newsletter_content):
    """
    Example function that sends newsletter content to a list of email subscribers.
    
    Args:
        subscriber_emails (list): List of subscriber email addresses
        newsletter_content (str): The newsletter content to send
    
    Returns:
        int: Number of emails successfully processed
    """
    success_count = 0
    
    for email in subscriber_emails:
        try:
            # Simulate sending email (in real app, use email libraries like smtplib)
            print(f"Sending newsletter to: {email}")
            print(f"Content: {newsletter_content[:50]}...")  # Show first 50 chars
            print("Email sent successfully!\n")
            success_count += 1
            
        except Exception as e:
            print(f"Failed to send email to {email}: {str(e)}\n")
    
    return success_count


# Example usage
if __name__ == "__main__":
    # Sample email list
    emails = [
        "john.doe@example.com",
        "jane.smith@company.org",
        "invalid-email",  # This will be marked as invalid
        "alice@techcorp.net",
        "bob.wilson@startup.io"
    ]
    
    # Sample message
    message = "Welcome to our newsletter!"
    
    print("=== Processing Emails with Message ===")
    results = process_emails_with_message(emails, message)
    
    print("\n=== Results Summary ===")
    for email, info in results.items():
        print(f"{email}: {info['status']}")
    
    print("\n=== Newsletter Example ===")
    newsletter_content = "This week's top stories: AI breakthroughs, new tech trends, and more!"
    success_count = send_newsletter_emails(emails[:3], newsletter_content)  # Use first 3 emails
    print(f"Successfully processed {success_count} emails")

