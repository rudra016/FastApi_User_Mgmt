import ssl
import pika
import json
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.database import SessionLocal
RABBITMQ_URL = "amqps://mrxifpeh:5ngDkk7VFF_rhmziwX0uW8jOzcyzQRLJ@collie.lmq.cloudamqp.com/mrxifpeh"
DATABASE_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "rudra6",
    "host": "localhost",
    "port": "5432",
}

def validate_user(user_id: int) -> bool:
    # Checks if the user exists using SQLAlchemy session.
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user is not None 

def process_message(body):
    data = json.loads(body)
    user_id = data.get("user_id")

    is_valid = validate_user(user_id)
    print(f"User Validation for ID {user_id}: {'Valid' if is_valid else 'Invalid'}")


params = pika.URLParameters(RABBITMQ_URL)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  

params.ssl_options = pika.SSLOptions(context)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue="user_validation_queue")
channel.basic_consume(queue="user_validation_queue", on_message_callback=process_message, auto_ack=True)

print("User Validation Service Running...")
channel.start_consuming()
