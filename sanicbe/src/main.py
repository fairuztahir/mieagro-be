import os
from sanic.response import json
from sanic_cors import CORS, cross_origin

import application

app = application.create(__name__)
CORS(app, automatic_options=True)


# Used as K8 health check.
@app.route("/ping", methods=['GET', 'OPTIONS'])
async def test(request):
    return json({"ping": "pong!"})

if __name__ == "__main__":
    debug_mode = os.getenv('APP_ENV', '') == 'dev'
    run_port = os.getenv('API_PORT', 5001)

    app.run(
        host='sanicbe',
        port=run_port,
        debug=debug_mode,
        access_log=debug_mode,
        auto_reload=debug_mode,
    )
