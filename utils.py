from django.core.paginator import Paginator

def get_page_object(objects, page=1, amount=25):
    pages = Paginator(objects, amount)
    if page < 1:
        page = 1
    elif page > pages.num_pages:
        page = pages.num_pages
    p = pages.page(page)

    return (p.object_list, pages.num_pages, amount, page)