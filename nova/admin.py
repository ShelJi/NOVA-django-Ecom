from django.contrib import admin
from nova.models import *

admin.site.register(UserdataModel)
admin.site.register(ProductData)
admin.site.register(ReviewModel)
admin.site.register(CartModel)
admin.site.register(OrdersModel)
admin.site.register(LatestDeals)