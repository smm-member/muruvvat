from . import models
def user_inf(request):
	if not request.user.is_anonymous:
		return {"my_user":models.Profile.objects.get(user=request.user)}
	return {"my_user":"my_user"}