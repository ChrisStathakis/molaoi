from django.conf.urls import url
from .views import *


urlpatterns =[
    url(r'^$',view=homepage),
    url(r'warehouse/giorgos/$',view=giorgos_reports),
    url(r'warehouse/$',view=warehouse),
    url(r'products/$',view=products),
    url(r'products/cat/(?P<dk>\d+)/$',view=products_category),
    url(r'products/vend/(?P<dk>\d+)/$',view=products_vendors),
    url(r'products/(?P<dk>\d+)/$',view=product_id),

    url(r'vendors/$',view=vendors),
    url(r'vendors/(?P<dk>\d+)/$',view=vendors_id),
    url(r'vendors-doy/(?P<dk>\d+)/$',view=vendors_per_doy),


    url(r'orders/$',view=orders),
    url(r'orders/(?P<dk>\d+)/$',view=order_id),
    url(r'orders-per-vendor/(?P<dk>\d+)/$',view=orders_per_category),

    url(r'restaurant-reports/$',view=restaurant_reports),
    url(r'restaurant-reports/resto-order/(?P<dk>\d+)/$',view=restaurant_order_specific),

    url(r'recipes-reports/$',view=restautant_recipes),


    url(r'outcome/$',view=outcome),

    url(r'outcome/payment-analysis/$',view=payment_analysis),

    url(r'outcome/logariasmoi/$',view=log_all),
    url(r'outcome/logariasmoi/(?P<dk>\d+)/$',view=log_all_id),

    url(r'outcome/μισθοδοσία/$',view=payroll_report),
    url(r'outcome/επιταγές/$',view=checks_reports),
    url(r'outcome/μισθοδοσία/analitika/$',view=misthosia_analisi),
    url(r'outcome/μισθοδοσία/ipal/(?P<dk>\d+)/$',view=misthodosia_ipal),
    url(r'outcome/μισθοδοσία/ocup/(?P<dk>\d+)/$',view=misthodosia_occup),


    url(r'outcome/pagia-agores/(?P<dk>\d+)/$',view=agoresEpiskeuesReport),
    url(r'outcome/pagia-agores/exoterikoi-synergates/$',view=exoterikoi_sinergates),

    url(r'income/$',view=reports_income),
    url(r'income/product/(?P<dk>\d+)/$',view=reports_specific_order),
    url(r'income/choose/(?P<yk>\d+)/(?P<mk>\d+)/(?P<dk>\d+)/$',view=reports_income_choose_specific_date),
    url(r'income/month/(?P<yk>\d+)/(?P<mk>\d+)/$',view=reports_income_choose_month),

    url(r'isologismos/$',view=isologismos,),


    url(r'balance-sheet-estimate/$',view=balance_sheet_estimate,),
    url(r'balance-sheet-estimate/current-month/$',view=balance_sheet_estimate_current_month,),
    url(r'balance-sheet-estimate/three-months/$',view=balance_sheet_estimate_current_three_months,),









    ]
