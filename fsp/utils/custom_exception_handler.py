from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from collections import defaultdict

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        if isinstance(exc, ValidationError):
            errors = []
            if isinstance(response.data, dict):
                for field, messages in response.data.items():
                    if isinstance(messages, list):
                        for message in messages:
                            errors.append(message)
                    else:
                        errors.append(messages)
            else:
                errors.append(str(response.data))
                
            response.data = {'errors': errors}
        else:
            response.data = {
                'errors': [str(msg) for msg in response.data.values()]
            }

    return response
