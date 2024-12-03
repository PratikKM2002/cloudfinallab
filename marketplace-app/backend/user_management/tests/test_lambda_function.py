import lambda_function

def test_lambda_handler():
    event = {}
    context = {}
    response = lambda_function.lambda_handler(event, context)
    assert response['statusCode'] == 200
