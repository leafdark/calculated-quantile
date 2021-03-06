from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from service import update_or_create_pool, calculate_quantile
from constant import POOL_ID, POOL_VALUES, PERCENTILE
from validate import float_range

app = Flask(__name__)
api = Api(app)

poll_post_args = reqparse.RequestParser()
poll_post_args.add_argument(POOL_ID, type=int, help="pool id", required=True)
poll_post_args.add_argument(POOL_VALUES, type=int, action='append', help="pool value array", required=True)

poll_calculator_args = reqparse.RequestParser()
poll_calculator_args.add_argument(POOL_ID, type=int, help="pool id", required=True)
poll_calculator_args.add_argument(PERCENTILE, type=float_range(0, 100), help="percentile of quantile", required=True)


class PoolClass(Resource):

    def post(self):
        args = poll_post_args.parse_args()
        is_updated = update_or_create_pool(args.get(POOL_ID), args.get(POOL_VALUES))
        status = "appended" if is_updated else "inserted"
        return {"status": status}


class PoolCalculatorClass(Resource):

    def post(self):
        args = poll_calculator_args.parse_args()
        res = calculate_quantile(args.get(POOL_ID), args.get(PERCENTILE))
        if res.get("is_error"):
            abort(500, message=res.get("msg"))
        return {"quantile": res.get("quantile"),
                "pool_size": res.get("size_arr")}


api.add_resource(PoolClass, "/pool")
api.add_resource(PoolCalculatorClass, "/pool-calculator")

if __name__ == "__main__":
    app.run(debug=True)
