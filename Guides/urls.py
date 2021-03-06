from django.conf.urls import patterns, url
from Guides.views.Profile import ProfileDetail, ProfileUpdate
from Guides.views.Review import ReviewCreate, ReviewDetail
from Guides.views.Tour import TourList, TourCreate, TourDetail, join_tour, leave_tour

urlpatterns = patterns('',
    url(r'^profile/(?P<pk>\d+)/$', ProfileDetail.as_view(), name='user.detail'),
    url(r'^profile/(?P<pk>\d+)/edit/$', ProfileUpdate.as_view(), name='user.edit'),
    url(r'^$', TourList.as_view(), name='tour.list'),
    url(r'^tour/create/$', TourCreate.as_view(), name='tour.create'),
    url(r'^tour/(?P<pk>\d+)/$', TourDetail.as_view(), name='tour.detail'),
    url(r'^tour/(?P<pk>\d+)/join/$', join_tour, name='tour.join'),
    url(r'^tour/(?P<pk>\d+)/leave/$', leave_tour, name='tour.leave'),
    url(r'^review/create/(?P<subject_pk>\d+)/$', ReviewCreate.as_view(), name='review.create'),
    url(r'^review/(?P<pk>\d+)/$', ReviewDetail.as_view(), name='review.detail')
)