from django.conf.urls import url
from django.urls import path, register_converter, re_path
from .views import *
from .utils import FourDigitYear


register_converter(FourDigitYear, "FourDigit")

urlpatterns = [
    path("list/", post_list),
    path("detail/<uuid:post_uuid>/", post_detail),
    path("detail/<int:post_id>/", post_detail),
    re_path(r"detail/(?P<post_slug>[/w-])+/", post_detail),
    path("categories/list/<slug:post_title>/", categories_list),
    # path("archive/<FourDigit:year>/", post_list),
    re_path(r"archive/(?P<year>[0-9]{4})/", post_list),
    path("archive/<int:year>/<int:month>/", post_list),
    re_path(r"gift/(?P<code>[0-9]{4})/", post_list),
    re_path(r"gift/(?P<code>[0-9]{6})/", post_list),
]
