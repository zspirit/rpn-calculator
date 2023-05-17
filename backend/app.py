from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource, Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import doc
from flask_cors import CORS
import re
import sys
import os

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Rpn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formula = db.Column(db.String(300), nullable=False)
    result = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Rpn {self.id}>'

    def serialize(self):
        return {"id": self.id,
                "formula": self.formula,
                "result": self.result,
                "created_at": self.created_at,}


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

def retrievData(data):
    res = []
    for item in data:
        res.append(item.serialize())
    return res

#  Restful way of creating APIs through Flask Restful
@ns.route('/<string:formula>')
class CalculatorAPI(MethodResource, Resource):
    @doc(description='Demo Calculator RPN API.', tags=['GET', 'Calculator', 'API'])
    def get(self, formula,):
        try:
            new_entry = Rpn(formula=formula, result=postfix(formula))
            db.session.add(new_entry)
            db.session.commit()

            return {'status': 'Success',
                    'code': 200,
                    'formula': formula,
                    'result': postfix(formula)}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'formula': formula,
                            'message': str(e)})


@ns.route('/rpn/list')
class CalculatorAPI(MethodResource, Resource):
    @doc(description='Rpn list.', tags=['GET', 'RPN', 'CALCULATOR'])
    def get(self, ):
        try:
            result = retrievData(Rpn.query.all())

            return {'status': 'Success',
                    'code': 200,
                    'result': result}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})


@ns.route('/rpn/list/<int:id>')
class CalculatorAPI(MethodResource, Resource):
    @doc(description='Retrieve RPN.', tags=['GET', 'RPN', 'CALCULATOR'])
    def get(self, id, ):
        address = ''
        try:
            rpn = Rpn.query.get_or_404(id)
            res = rpn.serialize()

            return {'status': 'Success',
                    'code': 200,
                    'RPN': res}
        except Exception as e:
            return jsonify({'status': 'Error',
                            'code': 400,
                            'message': str(e)})

@ns.route('/rpn/delete/<int:id>')
class CalculatorAPI(MethodResource, Resource):
    @doc(description='Delete Address.', tags=['DELETE', 'RPN', 'CALCULATOR'])
    def delete(self, id, ):
        rpn = Rpn.query.get_or_404(id)
        res = "Rpn " + str(id) + " was successfully deleted"
        try:
            db.session.delete(rpn)
            db.session.commit()
            return {'status': 'Success',
                    'code': 200,
                    'address': res}
        except:
            return 'There was an issue deleting rpn'

if __name__ == '__main__':
    app.run(debug=True)

