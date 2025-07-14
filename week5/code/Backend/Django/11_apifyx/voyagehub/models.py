from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    realm = models.CharField(max_length=100)  # e.g. “Elven Forest”
    description = models.TextField()
    is_visited = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
