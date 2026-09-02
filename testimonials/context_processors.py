from professors.models import Professor


def professor_context(request):
    """Adds is_professor flag to all template contexts."""
    is_professor = False
    if request.user.is_authenticated and request.user.email:
        is_professor = Professor.objects.filter(email__iexact=request.user.email).exists()
    return {'is_professor': is_professor}
