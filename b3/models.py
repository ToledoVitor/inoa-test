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

    def __str__(self) -> str:
        return self.code

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"
    

class Search(BaseSuperModel):
    SUPERIOR = "SUPERIOR"
    NEGOCIOS = "NEGOCIOS"
    INFERIOR = "INFERIOR" 

    PRICE_TUNNEL_CHOICES = {
        SUPERIOR: "SUPERIOR",
        NEGOCIOS: "NEGOCIOS",
        INFERIOR: "INFERIOR", 
    }
    price_tunnel = models.CharField(
        verbose_name="Túnel de Preço",
        max_length=20,
        choices=PRICE_TUNNEL_CHOICES,
        default="LAST_TRADED_PRICE",
    )

    stocks = models.ManyToManyField(
        Stock,
        blank=True,
        related_name="buscas",
        verbose_name="Ativos Monitorados"
    )

    interval = models.IntegerField(
        verbose_name="Intervalo entre buscas (minutos)",
        default=5,
    )

    task = models.OneToOneField(
        PeriodicTask, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self) -> str:
        return f"Busca - {self.pk}"

    class Meta:
        verbose_name = "Configuração de Busca"
        verbose_name_plural = "Configurações de Buscas"


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
    price = models.DecimalField(
        verbose_name="Preço do Ativo",
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.stock.code} - {self.price}"

    class Meta:
        verbose_name = "Preço do Ativo"
        verbose_name_plural = "Preços dos Ativos"
