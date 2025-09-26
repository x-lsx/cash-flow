from django.db import models

from smart_selects.db_fields import ChainedForeignKey
from django.core.exceptions import ValidationError
from django.utils import timezone

class FlowStatus(models.Model):
    
    name = models.CharField(max_length = 50, verbose_name = 'Статус')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Статус')  
        verbose_name_plural = ('Статусы')
        
        
class FlowType(models.Model):
    
    name = models.CharField(max_length = 50, verbose_name = 'Тип')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = ('Тип')
        verbose_name_plural = ('Типы')
       
class FlowCategory(models.Model):
    
    name = models.CharField(max_length = 50, verbose_name = 'Категория')
    type = models.ForeignKey(FlowType, on_delete = models.CASCADE, verbose_name = 'Тип')
        
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = ('Категория')
        verbose_name_plural = ('Категории')
        
class FlowSubcategory(models.Model):
    
    name = models.CharField(max_length = 50, verbose_name = 'Подкатегория')
    category = models.ForeignKey(FlowCategory, on_delete = models.CASCADE, verbose_name = 'Категория')
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = ('Подкатегория')
        verbose_name_plural = ('Подкатегории')
        

class Transaction(models.Model):
    
    status = models.ForeignKey(FlowStatus, on_delete = models.CASCADE,
                               verbose_name = 'Статус')
    type = models.ForeignKey(FlowType, on_delete = models.CASCADE,
                             verbose_name = 'Тип')
    category = ChainedForeignKey(
        FlowCategory, chained_field = 'type', chained_model_field = 'type',
        show_all = False, auto_choose = True, sort = True, verbose_name = 'Категория'
    )
    subcategory = ChainedForeignKey(
        FlowSubcategory, chained_field = 'category', chained_model_field = 'category',
        show_all = False, auto_choose = True, sort = True, verbose_name = 'Подкатегория'
    )
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = 'Сумма')
    comment = models.TextField(null = True, blank = True, verbose_name = 'Комментарий')
    created_at = models.DateField(default=timezone.now, verbose_name = 'Дата создания')
    
    def __str__(self):
        return f"{self.created_at} - {self.amount} руб."
    
    def clean(self):
        
        errors = {}
        if self.amount is not None and self.amount <= 0:
            errors["amount"] = "Сумма должна быть больше 0."

        # if self.category is not None and self.type is not None and self.category.type != self.type:
        #     errors["category"] = "Категория не относится к выбранному типу."

        # if self.subcategory and self.category and self.subcategory.category != self.category:
        #     errors["subcategory"] = "Подкатегория не относится к выбранной категории."

        if errors:
            raise ValidationError(errors)
        
    class Meta:
        verbose_name = 'Денежная транзакция'
        verbose_name_plural = 'Денежные транзакции'