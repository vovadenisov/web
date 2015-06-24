# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150512_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='img',
            field=models.ImageField(default=b'1.jpg', upload_to=b'/uploads/'),
            preserve_default=True,
        ),
    ]
