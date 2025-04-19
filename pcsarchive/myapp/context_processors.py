from .models import User

def user_sidebar_info(request):
    uid = request.session.get('user_id')
    if uid:
        try:
            user = User.objects.get(uid=uid)
            return {'user_profile': user}
        except User.DoesNotExist:
            return {}
    return {}