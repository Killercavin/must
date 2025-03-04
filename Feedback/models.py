from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import uuid

# Create your models here.
class FeedBackCategory(models.TextChoices):
    BUG_REPORT = 'BUG_REPORT','Bug Report'
    FEATURE_REQUEST = 'FEATURE_REQUEST','Feature Request'
    GENERAL_INQUIRY = 'GENERAL_INQUIRY','General Inquiry'
    ACCOUNT_ISSUE = 'ACCOUNT_ISSUE','Account Issue'
    PERFROMANCE_ISSUE = 'PERFOMANCE_ISSUE','Perfomance Issue'


class FeedBackPriority(models.TextChoices):
    LOW = 'LOW','Low'
    MEDIUM = 'MEDIUM','Medium'
    HIGH = 'HIGH','High'
    CRITICAL = 'CRITICAL','Critical'

class FeedBackStatus(models.TextChoices):
    PENDING = 'PENDING','Pending',
    IN_PROGRESS = 'IN_PROGRESS','In Progress'
    RESOLVED = 'RESOLVED','Resolved'

class FeedBack(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendee_id = models.CharField(max_length=255)
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment = models.CharField(
        max_length=20,
        choices=FeedBackCategory.choices,
        default=FeedBackCategory.GENERAL_INQUIRY
    )

    priority = models.CharField(
        max_length=10,
        choices=FeedBackPriority.choices,
        default=FeedBackPriority.MEDIUM,
    )
    status=models.CharField(
        max_length=15,
        choices=FeedBackStatus.choices,
        default=FeedBackStatus.PENDING
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback #{self.id} - {self.category}"
    

