# Generated by Django 4.2.20 on 2025-04-29 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('tech', 'テクノロジ系'), ('mgmt', 'マネジメント系'), ('strat', 'ストラテジ系')], default='tech', max_length=5, verbose_name='分野'),
        ),
    ]
