from django.db import models
from django.utils.text import slugify # Slug yaratmaq üçün

class Category(models.Model):
    """
    Menyu kateqoriyalarını saxlayır (məsələn, Burger, Pizza, Pasta, İçkilər).
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kateqoriya Adı"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True, # Admin panelində boş buraxmağa icazə verir, çünki avtomatik yaradacağıq
        help_text="URL-də görünəcək ad. Adı yazdıqda avtomatik yaranır."
    )

    class Meta:
        # Admin panelində modelin necə adlanacağı
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        # Siyahıda ada görə sıralansın
        ordering = ('name',)

    def __str__(self):
        # Admin panelində obyektin adı kimi bu görünsün
        return self.name

    def save(self, *args, **kwargs):
        # Obyekt yaddaşa yazılmamışdan əvvəl slug sahəsini avtomatik doldurur
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MenuItem(models.Model):
    """
    Menyudakı hər bir məhsulu təmsil edir.
    """
    categories = models.ManyToManyField(
        Category,
        related_name="menu_items",
        verbose_name="Kateqoriyalar",
        help_text="Məhsul bir neçə kateqoriyaya aid ola bilər."
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Məhsulun Adı"
    )
    description = models.TextField(
        verbose_name="Açıqlama",
        help_text="Məhsul haqqında qısa məlumat."
    )
    price = models.DecimalField(
        max_digits=7, # Məsələn, 99999.99
        decimal_places=2,
        verbose_name="Qiymət (AZN)"
    )
    image = models.ImageField(
        upload_to='menu_items/', # Yüklənən şəkillər `media/menu_items/` qovluğuna düşəcək
        verbose_name="Şəkil"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Mövcuddur?",
        help_text="Bu işarəli olarsa, məhsul menyuda görünəcək."
    )

    class Meta:
        verbose_name = "Menyu Məhsulu"
        verbose_name_plural = "Menyu Məhsulları"
        # Qiymətə görə artan sırada sıralansın
        ordering = ('price',)

    def __str__(self):
        return self.name


class BookTable(models.Model):
    """
    Saytdan gələn rezervasiyaları saxlayacaq model.
    """
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    name = models.CharField(max_length=200, verbose_name='Ad')
    phone = models.CharField(max_length=30, verbose_name='Telefon')
    email = models.EmailField(verbose_name='Email', blank=True)
    date = models.DateField(verbose_name='Rezervasiya tarixi')
    time = models.TimeField(verbose_name='Rezervasiya vaxtı')
    persons = models.PositiveSmallIntegerField(default=2, verbose_name='Neçə nəfər')
    message = models.TextField(blank=True, verbose_name='Qeyd')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi')

    class Meta:
        verbose_name = 'Rezervasiya'
        verbose_name_plural = 'Rezervasiyalar'
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name} — {self.date} {self.time} ({self.persons})"
    



class SiteSettings(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)
    logo_navbar = models.FileField(upload_to='core/site_settings',
                                   null=True, blank=True)

    logo_navbar_alt_data = models.CharField(max_length=255, null=True, blank=True,
                                            help_text='Add data for increasing SEO performance')

    logo_footer = models.FileField(upload_to='core/site_settings',
                                   null=True, blank=True)
    footer_title = models.CharField(max_length=255, null=True, blank=True)
    footer_subtitle = models.CharField(max_length=255, null=True, blank=True)

    logo_footer_alt_data = models.CharField(max_length=255, null=True, blank=True,
                                            help_text='Add data for increasing SEO performance')

    favicon = models.FileField(upload_to='core/site_settings', null=True, blank=True)
    favicon_alt_data = models.CharField(max_length=255, null=True, blank=True,
                                        help_text='Add data for increasing SEO performance')

    address = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=15, null=True, blank=True)
    iframe = models.TextField(help_text="Just paste iframe src data from googlemap", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='Enter phone number starting with the code')

    fax = models.CharField(max_length=255, null=True, blank=True,
                                    help_text='Enter fax number starting with the code')

    facebook = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your facebook url')
    instagram = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your instagram url')
    twitter = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your twitter url')
    linkedin = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your linkedin url')
    youtube = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your youtube url')
    website = models.URLField(max_length=255, null=True, blank=True, help_text='Enter your website url')


    def __str__(self):
        return self.company_name
    class Meta:
        verbose_name_plural = "Site Settings"    