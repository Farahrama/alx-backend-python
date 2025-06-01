# messaging_app/chats/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Override id with UUID
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # إضافات غير موجودة في AbstractUser (لو محتاجين)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # AbstractUser عنده أصلاً email, password, first_name, last_name
    # لو عايز تغيّر حاجة أو تضيف حقول، تضيف هنا

    USERNAME_FIELD = "username"  # أو email لو عايز تستخدم الإيميل كيوزر
    REQUIRED_FIELDS = []  # مثلاً email لو عايز
    
    def __str__(self):
        return self.username

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    
    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
