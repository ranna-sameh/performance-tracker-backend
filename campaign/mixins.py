from rest_framework.exceptions import ValidationError


def validate_ordering(model, ordering: str) -> bool:
    """
    Validate that the provided ordering attribute is a valid field
    for ordering in the model.

    :param model: The Django model.
    :param ordering: The ordering attribute to validate.

    :return: True if the ordering attribute is valid; False otherwise.
    """
    # List of valid fields for ordering
    valid_fields = [field.name for field in model._meta.get_fields()]
    # If the ordering attribute contains a hyphen for descending sorting, remove it
    if '-' in ordering:
        ordering = ordering.replace('-', '')
    return ordering in valid_fields


class OrderingMixin:
    """
    Mixin class to handle ordering logic for views.
    """

    @staticmethod
    def get_ordered_queryset(request, queryset, model):
        """
        Apply ordering to the queryset based on the request's query parameters.

        :param request: The request object.
        :param queryset: The queryset to be ordered.
        :param model: The Django model.

        :return: The ordered queryset.
        """
        ordering = request.query_params.get('ordering')
        if ordering:
            is_valid = validate_ordering(model, ordering)
            if not is_valid:
                raise ValidationError({'error': 'Invalid ordering attribute.'})
            queryset = queryset.order_by(ordering)
        return queryset
