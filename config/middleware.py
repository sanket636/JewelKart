import logging
import time
import uuid


logger = logging.getLogger(
    'jewelkart.api'
)


class ApiRequestLoggingMiddleware:

    def __init__(
        self,
        get_response
    ):

        self.get_response = (
            get_response
        )


    def __call__(
        self,
        request
    ):

        # Only process REST APIs
        if not request.path.startswith(
            '/api/'
        ):

            return self.get_response(
                request
            )


        request_id = (

            request.headers.get(
                'X-Request-ID'
            )

            or

            uuid.uuid4().hex
        )


        request.request_id = (
            request_id
        )


        start_time = (
            time.perf_counter()
        )


        # Request goes to API here
        response = (
            self.get_response(
                request
            )
        )


        duration_ms = (

            time.perf_counter()
            -
            start_time

        ) * 1000


        response[
            'X-Request-ID'
        ] = request_id


        response[
            'X-Response-Time-ms'
        ] = (
            f'{duration_ms:.2f}'
        )


        user = getattr(
            request,
            'user',
            None
        )


        if (
            user
            and
            user.is_authenticated
        ):

            username = (
                user.username
            )

        else:

            username = (
                'anonymous'
            )


        logger.info(

            'request_id=%s '
            'method=%s '
            'path=%s '
            'status=%s '
            'duration_ms=%.2f '
            'user=%s',

            request_id,

            request.method,

            request.path,

            response.status_code,

            duration_ms,

            username
        )


        return response