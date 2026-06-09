from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_deal'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='component_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('', 'Not a builder part'),
                    ('cpu', 'Processor (CPU)'),
                    ('mobo', 'Motherboard'),
                    ('gpu', 'Graphics Card (GPU)'),
                    ('ram', 'System Memory (RAM)'),
                    ('storage', 'Storage (SSD)'),
                    ('psu', 'Power Supply (PSU)'),
                    ('cooler', 'CPU Cooler'),
                    ('case', 'Chassis Case'),
                ],
                default='',
                help_text='PC Builder slot — only used when "Show in PC Builder" is enabled',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='is_builder_part',
            field=models.BooleanField(default=False, help_text='Include this product in the PC Builder'),
        ),
        migrations.AddField(
            model_name='product',
            name='socket',
            field=models.CharField(blank=True, help_text='CPU/Motherboard socket, e.g. AM5, LGA1700', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='wattage',
            field=models.PositiveIntegerField(default=0, help_text='Power draw in watts (PSU = total capacity)'),
        ),
    ]
