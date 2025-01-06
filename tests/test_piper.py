import unittest
import json
from unittest.mock import patch, mock_open
from datetime import datetime
from pdb import set_trace

from col.comm.piper import (Headers, Endpoint, Message, Tool, Parameters,
                            Request)

class TestPiper(unittest.TestCase):
    def setUp(self):
        """Initialize test data"""
        self.headers = {'Content-Type': 'application/json'}
        self.url = 'http://example.com'
        self.endpoint = Endpoint(url=self.url, header=self.headers)
        self.header_obj = Headers()

    def test_endpoint_attributes(self):
        """Test endpoint URL and header attributes"""
        self.assertEqual(self.endpoint.url, self.url)
        self.assertEqual(self.endpoint.header, self.headers)

    def test_headers_empty_initialization(self):
        """Test initialization of empty Headers object"""
        empty_headers = Headers()
        self.assertEqual(empty_headers.get_all_headers(), {})

    def test_headers_with_data_initialization(self):
        """Test initialization of Headers object with data"""
        headers_with_data = Headers(self.headers)
        self.assertEqual(headers_with_data.get_all_headers(), self.headers)

    def test_header_operations(self):
        """Test adding, getting and removing headers"""
        # Add and get header
        self.header_obj.add_header('Authorization', 'Bearer token123')
        self.assertEqual(self.header_obj.get_header('Authorization'), 'Bearer token123')

        # Remove header
        self.header_obj.remove_header('Authorization')
        self.assertIsNone(self.header_obj.get_header('Authorization'))

        # Get non-existent header
        self.assertIsNone(self.header_obj.get_header('Non-Existent'))

    def test_header_bulk_operations(self):
        """Test bulk operations on headers"""
        # Update multiple headers
        test_headers = {'header1': 'value1', 'header2': 'value2'}
        self.header_obj.update_headers(test_headers)
        self.assertEqual(self.header_obj.get_all_headers(), test_headers)

        # Update existing headers
        update_headers = {'header1': 'updated', 'header3': 'value3'}
        self.header_obj.update_headers(update_headers)
        self.assertEqual(self.header_obj.get_header('header1'), 'updated')
        self.assertEqual(self.header_obj.get_header('header3'), 'value3')

        # Clear all headers
        self.header_obj.clear_headers()
        self.assertEqual(self.header_obj.get_all_headers(), {})

    def test_tool_initialization(self):
        """Test Tool class initialization and attributes"""
        tool_type = "function"
        function_name = "test_function"
        description = "Test description"
        parameters = {"param1": "value1"}

        tool = Tool(tool_type, function_name, description, parameters)

        self.assertEqual(tool.type, tool_type)
        self.assertEqual(tool.function["name"], function_name)
        self.assertEqual(tool.function["description"], description)
        self.assertEqual(tool.function["parameters"], parameters)

    def test_messages_initialization(self):
        """Test Messages class initialization and attributes"""
        role = "user"
        content = "Test message content"

        message = Message(role, content)

        self.assertEqual(message.role, role)
        self.assertEqual(message.content, content)

    def test_parameters_initialization_default_values(self):
        """Test Parameters class initialization with default values"""
        params = Parameters()

        self.assertIsNone(params.model)
        self.assertEqual(params.messages, [])
        self.assertIsNone(params.max_tokens)
        self.assertEqual(params.temperature, 0.7)
        self.assertEqual(params.top_p, 0.95)
        self.assertIsNone(params.top_k)
        self.assertEqual(params.presence_penalty, 0.0)
        self.assertEqual(params.frequency_penalty, 0.0)
        self.assertIsNone(params.stop)
        self.assertIsNone(params.tools)
        self.assertIsNone(params.tool_choice)
        self.assertIsNone(params.response_format)
        self.assertIsNone(params.seed)
        self.assertIsNone(params.transforms)
        self.assertEqual(params.stream, False)

    def test_parameters_initialization_with_values(self):
        """Test Parameters class initialization with custom values"""
        custom_params = {
            'model': 'gpt-4',
            'messages': ['message1', 'message2'],
            'max_tokens': 100,
            'temperature': 0.8,
            'top_p': 0.9,
            'top_k': 40,
            'presence_penalty': 0.1,
            'frequency_penalty': 0.2,
            'stop': ['stop1', 'stop2'],
            'tools': ['tool1', 'tool2'],
            'tool_choice': 'auto',
            'response_format': 'json',
            'seed': 123,
            'transforms': ['t1', 't2'],
            'stream': True
        }

        params = Parameters(**custom_params)

        for key, value in custom_params.items():
            self.assertEqual(getattr(params, key), value)

    def test_parameters_partial_initialization(self):
        """Test Parameters class initialization with partial parameters"""
        partial_params = {
            'model': 'gpt-3.5-turbo',
            'max_tokens': 50,
            'temperature': 0.5
        }

        params = Parameters(**partial_params)

        # Test provided values
        self.assertEqual(params.model, 'gpt-3.5-turbo')
        self.assertEqual(params.max_tokens, 50)
        self.assertEqual(params.temperature, 0.5)

        # Test default values
        self.assertEqual(params.messages, [])
        self.assertEqual(params.top_p, 0.95)
        self.assertEqual(params.stream, False)

class TestPiper(unittest.TestCase):
    def test_request_initialization(self):
        params = Parameters(model="test-model", messages=[], max_tokens=100)
        endpoint = Endpoint(url="http://test.com", header={"key": "value"})
        request = Request(parameters=params, endpoint=endpoint)

        self.assertIsInstance(request.parameters, Parameters)
        self.assertIsInstance(request.endpoint, Endpoint)

    def test_parameters_initialization(self):
        parameters = Parameters(
            model="test-model",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=100,
            temperature=0.8,
            top_p=0.9,
            presence_penalty=0.1,
            frequency_penalty=0.1,
            stream=True
        )

        self.assertEqual(parameters.model, "test-model")
        self.assertEqual(len(parameters.messages), 1)
        self.assertEqual(parameters.params['max_tokens'], 100)
        self.assertEqual(parameters.params['temperature'], 0.8)
        self.assertEqual(parameters.params['top_p'], 0.9)
        self.assertEqual(parameters.params['presence_penalty'], 0.1)
        self.assertEqual(parameters.params['frequency_penalty'], 0.1)
        self.assertTrue(parameters.params['stream'])

    def test_endpoint_initialization(self):
        endpoint = Endpoint(url="http://test.com", header={"Authorization": "Bearer token"})

        self.assertEqual(endpoint.url, "http://test.com")
        self.assertEqual(endpoint.header, {"Authorization": "Bearer token"})

    def test_headers_operations(self):
        headers = Headers({"Content-Type": "application/json"})

        headers.add_header("Authorization", "Bearer token")
        self.assertEqual(headers.get_header("Authorization"), "Bearer token")

        headers.remove_header("Content-Type")
        self.assertIsNone(headers.get_header("Content-Type"))

        headers.update_headers({"Accept": "application/json"})
        self.assertEqual(headers.get_all_headers(),
                        {"Authorization": "Bearer token", "Accept": "application/json"})

        headers.clear_headers()
        self.assertEqual(headers.get_all_headers(), {})

    def test_tool_initialization(self):
        tool_params = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }

        tool = Tool(
            tool_type="function",
            function_name="get_user",
            description="Get user information",
            parameters=tool_params
        )

        self.assertEqual(tool.type, "function")
        self.assertEqual(tool.function["name"], "get_user")
        self.assertEqual(tool.function["description"], "Get user information")
        self.assertEqual(tool.function["parameters"], tool_params)

    def test_messages_initialization(self):
        message = Message(role="user", content="Hello, AI!")

        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Hello, AI!")
