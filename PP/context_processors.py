from .models import Notification


def get_notifications(request):
	if request.user.is_authenticated:
		notifies = Notification.objects.filter(receiver_id=request.user, is_read=False)
		return {'notifies': notifies}
	else:
		return {'notifies': 0}