
from django.contrib import admin
from .models import Category, MenuItem, BookTable, SiteSettings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Kateqoriya modelinin admin panelində görünüşünü tənzimləyir.
    """
    # Siyahıda hansı sütunların görünəcəyini təyin edir.
    list_display = ('name', 'slug')

    # 'slug' sahəsinin 'name' sahəsinə görə avtomatik dolmasını təmin edir.
    # Ad yazdıqca slug sahəsi canlı olaraq dolacaq.
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    MenuItem modelinin admin panelində görünüşünü tənzimləyir.
    """
    # Siyahıda məhsulun adını, kateqoriyasını, qiymətini və mövcudluğunu göstərir.
    list_display = ('name', 'price', 'is_available')

    # Siyahının özündəcə qiyməti və mövcudluq statusunu dəyişməyə imkan verir.
    # Bu, sürətli redaktə üçün çox faydalıdır.
    list_editable = ('price', 'is_available')

    # Sağ tərəfdə kateqoriyaya və mövcudluğa görə sürətli filtrasiya paneli əlavə edir.
    # Yüzlərlə məhsul olanda bu çox vacibdir.
    list_filter = ('categories', 'is_available')

    # Məhsul adına və açıqlamasına görə axtarış etmək üçün axtarış qutusu əlavə edir.
    search_fields = ('name', 'description')


@admin.register(BookTable)
class BookTableAdmin(admin.ModelAdmin):
    """Admin üçün rezervasiya qeydlərini idarə etmə sinifi."""
    list_display = ('name', 'phone', 'date', 'time', 'persons', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('created_at',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Manage site-wide settings from admin."""
    list_display = ('company_name', 'email', 'phone_number')
    readonly_fields = ()
    fieldsets = (
        (None, {
            'fields': ('company_name', 'logo_navbar', 'logo_navbar_alt_data', 'logo_footer', 'logo_footer_alt_data', 'favicon', 'favicon_alt_data')
        }),
        ('Contact & Social', {
            'fields': ('address', 'phone_number', 'email', 'facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'website')
        }),
        ('Map & Footer', {
            'fields': ('iframe', 'footer_title', 'footer_subtitle')
        }),
    )