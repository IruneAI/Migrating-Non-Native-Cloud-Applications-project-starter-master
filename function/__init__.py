## This folder will contains the Azure function code.

## Note:

#- Before deploying, be sure to update your requirements.txt file by running `pip freeze > requirements.txt`
#- Known issue, the python package `psycopg2` does not work directly in Azure; install `psycopg2-binary` instead to use the `psycopg2` library in Azure

#The skelton of the `__init__.py` file will consist of the following logic:


import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)


    try:
        # Stablish connection to database
        conn = psycopg2.connect(host="techconfdbserver.postgres.database.azure.com", database="techconfdb", user="iruadmin@techconfdbserve", password="!Iru1234"
        with conn.cursor() as db_cursor:
            # select notification message and subject from database using the notification_id
            notification = db_cursor.execute("SELECT message, subject FROM public.notification WHERE id = %s", (notification_id,))
            # select attendees email and name
            db_cursor.execute("SELECT email, first_name, last_name FROM public.attendee")
            attendees = db_cursor.fetchall()
            #Loop through each attendee and send an email with a personalized subject
            #for attendee in attendees:
                #send email


        # update the notification table by setting the completed date and updating the status with the total number of attendees notified 
            db_cursor.execute("UPDATE public.notification SET completed_date = %s, status = %s WHERE id = %s", (datetime.utcnow(), 'Notified {} attendees'.format(len(attendees)), notification_id,))
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        #closing connection
        conn.close()

