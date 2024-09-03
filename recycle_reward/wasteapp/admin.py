from django.contrib import admin

# Register your models here.


from .models import user, Waste, PlasticWaste, MetalWaste, PaperWaste, Order

admin.site.register(user)
admin.site.register(Waste)
admin.site.register(PlasticWaste)
admin.site.register(MetalWaste)
admin.site.register(PaperWaste)
admin.site.register(Order)

