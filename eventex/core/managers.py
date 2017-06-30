from django.db import models


class KindQuerySet(models.QuerySet):
    def phones(self):
        return self.filter(kind=self.model.PHONE)

    def emails(self):
        return self.filter(kind=self.model.EMAIL)



