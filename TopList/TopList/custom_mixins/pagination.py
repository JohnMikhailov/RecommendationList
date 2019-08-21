class PaginationMixin:
    use_pagination = True

    def paginate_queryset(self, queryset):
        if not self.use_pagination:
            return None
        return super().paginate_queryset(queryset)
