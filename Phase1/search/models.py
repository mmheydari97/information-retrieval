from django.db import models


# Create your models here.
class News(models.Model):
    doc_id = models.IntegerField(primary_key=True, default=0)
    publish_date = models.DateTimeField()

    # max length in dataset is 195
    title = models.CharField(max_length=256, null=False)
    url = models.URLField()

    # max length in dataset is 651
    summary = models.TextField()

    # max length in dataset is 319
    meta_tags = models.CharField(max_length=350)
    content = models.TextField()
    thumbnail = models.URLField()

    def __str__(self):
        return str(self.title)
