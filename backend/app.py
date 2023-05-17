from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_cors import CORS
import re
import sys

app = Flask(__name__)  # Flask app instance initiated
CORS(app)
api = Api(app,
          version='1.0',
          title='Simple RPN Calculator API',
          description='This is a simple demo RPN calculator API ')  # Flask restful wraps Flask app around it.
ns = api.namespace('/',
                   description='Demo : Simple RPN Calculator')
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='RPN Calculator Demo',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


def calculate(operator, op_x, op_y):
    """ compute basic arithmetic operations """
    cases = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    return cases[operator](op_x, op_y)

def postfix(expression):
    """ compute postfix expression """
    res         = 0
    stack       = []
    elements    = re.split(r"\s+", expression)

    for elem in elements:
        if re.match("^[-+\\/*()]$", elem):
            op1 = stack.pop()
            op2 = stack.pop()
            res = calculate(elem, int(op2), int(op1))
            stack.append(res)
        else:
            stack.append(elem)
    return res




#  Restful way of creating APIs through Flask Restful
@ns.route('/<string:formula>')
class CalculatorAPI(MethodResource, Resource):
    @doc(description='Demo Calculator RPN API.', tags=['GET', 'Calculator', 'API'])
    def get(self, formula,):
        try:
            return {'status': 'Success',
                    'code': 200,
                    'formula': formula,
                    'result': postfix(formula)}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'formula': formula,
                            'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

