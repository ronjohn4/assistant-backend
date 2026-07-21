from app import flask_api
from flask_restful import Resource, reqparse
from flask import current_app
from app.tools.orchestrator import Orchestrator

agent_orchestrator = Orchestrator()

# helper functions -------------------------------------
def actions_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("query", type=str, required=True, help="query problem (required)")
    return parser


# agent routes -------------------------------------
class Agent(Resource):
    def post(self):
        current_app.logger.debug(f'/agent post')
        parser = actions_parser()
        args = parser.parse_args()
        query = args["query"]
        current_app.logger.debug(f"/agent post args: {args}")

        r = agent_orchestrator.ask(query=query)
        return r, 200


flask_api.add_resource(Agent, '/agent') #post


# healthcheck routes -------------------------------------
class HealthCheck(Resource):
    def get(self):
        current_app.logger.debug(f'/health get')
        try:
            # TODO - what to do for a test?
            current_app.logger.info(f"/health get: 200")
            return'{"status": "ok"}', 200
        except Exception as e:
            current_app.logger.error(f"/health get: {e}")
            return'{"status": "fail"}', 503

flask_api.add_resource(HealthCheck, '/health')
