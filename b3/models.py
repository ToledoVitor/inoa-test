from datetime import timezone

from django.db import models
from django_celery_beat.models import PeriodicTask


class BaseSuperManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class BaseSuperModel(models.Model):
    # Logical delete para manter registros no banco
    deleted = models.BooleanField(verbose_name="Deletado", default=False, db_index=True)
    deleted_at = models.DateTimeField(
        verbose_name="Deletado às", blank=True, null=True, default=None
    )

    created_at = models.DateTimeField(verbose_name="Criado às", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Atualizado às", auto_now=True)

    # managers
    objects = BaseSuperManager()
    objects_all = models.Manager()

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def delete(self, force=False):
        if force:
            return super().delete()

        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Stock(BaseSuperModel):
    code = models.CharField(verbose_name="Código do ativo", max_length=10, unique=True)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"
    

class Search(BaseSuperModel):
    stocks = models.ManyToManyField(
        Stock,
        null=True,
        blank=True,
        related_name="buscas",
        verbose_name="Ativos Monitorados"
    )
    all_stocks = models.BooleanField(verbose_name="Todos os ativos", default=False)

    interval = models.IntegerField(
        verbose_name="Intervalo entre buscas (minutos)",
        default=5,
    )

    task = models.OneToOneField(
        PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Configuração de Busca"
        verbose_name_plural = "Configurações de Buscas"


class SearchRequest(models.Model):
    response_time = models.IntegerField(
        verbose_name="Tempo da resposta",
        blank=False,
    )
    response_status = models.IntegerField(
        verbose_name="Status da resposta",
        blank=False,
    )
    search = models.ForeignKey(Search, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Resposta da Busca"
        verbose_name_plural = "Respostas das Buscas"


class StockPrice(BaseSuperModel):
    stock = models.ForeignKey(
        Stock,
        related_name="prices",
        verbose_name="Preço do Ativo",
        on_delete=models.CASCADE,
    )
    search = models.ForeignKey(
        Search,
        related_name="prices",
        verbose_name="Configuração de Busca",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Preço do Ativo"
        verbose_name_plural = "Preços dos Ativos"
