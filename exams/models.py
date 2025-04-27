from django.db import models

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'テクノロジ系'),
        ('mgmt', 'マネジメント系'),
        ('strat', 'ストラテジ系'),
    ]

    text        = models.TextField('問題文')
    choice_a    = models.CharField('選択肢 A', max_length=255)
    choice_b    = models.CharField('選択肢 B', max_length=255)
    choice_c    = models.CharField('選択肢 C', max_length=255)
    choice_d    = models.CharField('選択肢 D', max_length=255)
    correct     = models.CharField('正解', max_length=1,
                                   choices=[('a','A'), ('b','B'), ('c','C'), ('d','D')])
    category    = models.CharField('分野', max_length=5, choices=CATEGORY_CHOICES, default='tech')
    category = models.CharField(max_length=32, default='unknown')   # 既存
    # 追加すると便利
    exam_year  = models.CharField(max_length=8, default='')
    exam_part  = models.CharField(max_length=16, default='')
    def __str__(self):
        return self.text[:30]
