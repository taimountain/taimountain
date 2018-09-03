from apistar import App, Route, http, exceptions


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


def homepage() -> str:
    return '<html><body><h1>Homepage</h1></body></html>'


def echo_request_info(request: http.Request) -> dict:
    return {
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'body': request.body.decode('utf-8')
    }


def echo_query_params(query_params: http.QueryParams) -> dict:
    print(query_params)
    return {
        'params': dict(query_params)
    }


def hello_world(accept_language: http.Header) -> http.JSONResponse:
    if 'de' in accept_language:
        data = {'text': 'Hallo, Welt!'}
    else:
        data = {'text': 'Hello, world!'}
    headers = {'Vary': 'Accept-Language'}
    return http.JSONResponse(data, status_code=200, headers=headers)


def echo_username(username: str) -> dict:
    return {'message': 'Welcome, %s!' % username}


USERS = {1: 'hazel', 2: 'james', 3: 'ana'}


def list_users(app: App) -> list:
    return [
        {
            'username': username,
            'url': app.reverse_url('get_user', user_id=user_id)
        } for user_id, username in USERS.items()
    ]


def get_user(app: App, user_id: int) -> dict:
    if user_id not in USERS:
        raise exceptions.NotFound()
    return {
        'username': USERS[user_id],
        'url': app.reverse_url('get_user', user_id=user_id)
    }


routes = [
    Route('/', method='GET', handler=welcome),
    Route('/home', method='GET', handler=homepage),
    Route('/request', method='GET', handler=echo_request_info),
    Route('/query', method='GET', handler=echo_query_params),
    Route('/hello', method='GET', handler=hello_world),
    Route('/users/{username}/', method='GET', handler=echo_username),
    Route('/users/', method='GET', handler=list_users),
    Route('/users/{user_id}/', method='GET', handler=get_user)

]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
