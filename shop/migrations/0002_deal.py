import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('discount_label', models.CharField(blank=True, help_text='e.g. 15% OFF', max_length=50)),
                ('badge', models.CharField(blank=True, help_text='e.g. FLASH SALE', max_length=50)),
                ('starts_at', models.DateTimeField()),
                ('ends_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('products', models.ManyToManyField(blank=True, related_name='deals', to='shop.product')),
            ],
            options={
                'ordering': ['-starts_at'],
            },
        ),
    ]
