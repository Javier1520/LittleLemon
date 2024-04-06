from rest_framework.pagination import PageNumberPagination

class MenuItemPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 5
    page_size_query_param = 'perpage'
    page_query_param = 'page'