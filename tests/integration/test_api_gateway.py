import os
import boto3
import pytest
import requests

class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("TESTING_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the TESTING_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "VisitorCountApi"]

        if not api_outputs:
            raise KeyError(f"VisitorCountApi not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_api_gateway_get(self, api_gateway_url):
        response = requests.get(api_gateway_url + '/count')
        assert response.status_code == 200
        assert response.json() > 0

    def test_api_gateway_post(self, api_gateway_url):
        responseGet = requests.get(api_gateway_url + '/count')
        getValue = responseGet.json()

        response = requests.post(api_gateway_url + '/count')
        assert response.status_code == 200
        assert response.json() == getValue + 1
