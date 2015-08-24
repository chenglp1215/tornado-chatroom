import os

TORNADO_SETTINGS = dict(
	# debug=True,
    login_url='/login',
    post_login_redirect_url='/',
    cookie_secret='bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    template_path=os.path.join(os.path.dirname(__file__), "templates")
)

