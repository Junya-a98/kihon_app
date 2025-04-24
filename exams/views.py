from django.shortcuts import render
from django.db import models
class Question(models.Model):
    """午前試験タイプ（四択）だけを想定した最小モデル"""
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

    def __str__(self) -> str:
        return self.text[:30]  # 一覧表示用

# Create your views here.
