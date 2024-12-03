
import os
import boto3


ses_client = boto3.client('ses', region_name='us-east-2')

def send_email_ses(body_text, ticket_details):
   
    email = ticket_details['ticket_user_id']
    user_name = ticket_details['ticket_user_id']
    movie_name = ticket_details['ticket_movie_id']
    showtime = ticket_details['ticket_showtime']
    
    subject = "Booking Confirmation for {movie_name}".format(movie_name=movie_name)

    body_text = "Hello {user_name}, booking confirmed for {movie_name} on {showtime}".format(user_name=user_name, movie_name=movie_name, showtime=showtime)
    response = ses_client.send_email(
                Source=os.environ['SES_SENDER_EMAIL'],
                Destination={
                    'ToAddresses': [email]  
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text
                        }
                    }
                }
            )
    print(f"Email sent! Message ID: {response['MessageId']}")
    
    return response


