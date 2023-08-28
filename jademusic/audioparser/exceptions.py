http_exceptions = {
	400: 'Bad Request',
	401: 'Unauthorized',
	403: 'Forbidden',
	404: 'Not Found',
	500: 'Internal Server Error',
	504: 'Gateway Time-out'
}


def handle_exception(request, logger, exception, console_obj, error_msg=None, http_status=500):
	logger.error(exception)
	request.status_code = http_status

	request.data['status'] = http_status
	request.data['status_string'] = http_exceptions[http_status]
	request.data['error'] = str(exception)

	if error_msg:
		request.data['error_message'] = error_msg
		console_obj.print(f'[bold red]{error_msg}[/]')
	else:
		console_obj.print(f'[bold red]Error occured in {logger.name} | {exception.__class__.__name__}: {exception}[/]')
