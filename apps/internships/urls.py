from django.urls import path
from .views import (
    InternshipListCreateView,
    InternshipRetrieveUpdateDestroyView,
    ApplicationListCreateView,
    InternshipApplicationListView,
    WithdrawApplicationView,
)

urlpatterns = [
    path("", InternshipListCreateView.as_view(), name="list_create_internship"),
    path(
        "<uuid:id>/",
        InternshipRetrieveUpdateDestroyView.as_view(),
        name="retrieve_update_destroy_internship",
    ),
    path(
        "<uuid:internship_id>/apply_internship/",
        ApplicationListCreateView.as_view(),
        name="apply_internship",
    ),
    path(
        "<uuid:internship_id>/view_all_applications/",
        InternshipApplicationListView.as_view(),
        name="view_all_applications",
    ),
    path(
        "<uuid:id>/withdraw_internship/",
        WithdrawApplicationView.as_view(),
        name="withdraw_internship",
    ),
]
