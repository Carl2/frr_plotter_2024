#!/usr/bin/env python

import socket
import json
import urllib3
from enum import StrEnum

"""The idea is to create a pipeline design to communicate with AI

overview
----------


"""



class ContentType(StrEnum):
    JSON = "application/json"
    FORM_DATA = "multipart/form-data"
    OCTET_STREAM = "application/octet-stream"
    TEXT_PLAIN = "text/plain"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    CSV = "text/csv"

class Headers:
    def __init__(self, content_type=ContentType.JSON, headers_dict=None):
        if headers_dict is None:
            headers_dict = {}
        self.headers = headers_dict
        self.content_type = content_type

    def add_header(self, key, value):
        self.headers[key] = value

    def remove_header(self, key):
        self.headers.pop(key, None)

    def get_header(self, key):
        return self.headers.get(key)

    def get_all_headers(self):
        return self.headers

    def update_headers(self, new_headers):
        self.headers.update(new_headers)

    def clear_headers(self):
        self.headers.clear()

    def __repr__(self):
        header_dict = "\n".join(f"{key}: {value}" for key,value in self.headers.items())

        return f"Content-type: {self.content_type}\n{header_dict}"

class Endpoint:
    def __init__(self,*, url:str , header: Headers):
        self.url = url
        self.header = header


class Tool:
    def __init__(self, tool_type, function_name, description, parameters):
        self.type = tool_type
        self.function = {
            "name": function_name,
            "description": description,
            "parameters": parameters
        }

        # TODO: Fix!
        def __repr__(self):
            return f"N/A yet"


class Message:
    def __init__(self,*, role, content):
        self.role = role
        self.content = content
    def __repr__(self):
        return f"{self.role}: {self.content}"


class Parameters:
    def __init__(self, *, model: str, messages: list[Message], **kwargs):
        self.model = model
        self.messages = messages
        self.params = {
            'max_tokens': kwargs.get('max_tokens'),
            'temperature': kwargs.get('temperature', 0.7),
            'top_p': kwargs.get('top_p', 0.95),
            'top_k': kwargs.get('top_k'),
            'presence_penalty': kwargs.get('presence_penalty', 0.0),
            'frequency_penalty': kwargs.get('frequency_penalty', 0.0),
            'stop': kwargs.get('stop'),
            'tools': kwargs.get('tools'),
            'tool_choice': kwargs.get('tool_choice'),
            'response_format': kwargs.get('response_format'),
            'seed': kwargs.get('seed'),
            'transforms': kwargs.get('transforms'),
            'stream': kwargs.get('stream', False)
        }

    def __repr__(self):
        messages_str = "\n".join(repr(message) for message in self.messages)
        tools_str = "\n".join(repr(tool) for tool in self.tools)
        return f"""
Parameters:
model={self.model},
messages:
{messages_str},
params={self.params})
"""


class Request:
    def __init__(self,*, parameters, endpoint ):
        self.parameters = parameters
        self.endpoint = endpoint



#######################################################################
#                          Openrouter request                         #
#######################################################################

def create_openrouter_request(*,url:str ,key:str , model:str, messages: list[Message] ):
    header = Headers( ContentType.JSON,
        {
        "Authorization": f"Bearer {key}",

    })

    endpoint = Endpoint(url=url, header=header)

    parameters = Parameters( messages=messages, tools=None, model=model)
    return Request(parameters=parameters, endpoint=endpoint)







def TestingStream1(args):
     http = urllib3.PoolManager()

     headers = {
          "Content-Type": "application/json",
          "Client-Request-ID": "23040"
      }

     data = json.dumps({
        "model": "qwen2.5-coder:latest",
        "prompt": "What are the consequences of AI?",
        "stream": True
    })

     response = http.request(
          method="POST",
          url="http://localhost:11434/api/generate",
          headers=headers,
          body=data,
          preload_content=False
     )
     print(f"{response.status}, {response.headers},\n\n {response.data.decode('utf-8')}")

def TestingStreams2():
    http = urllib3.PoolManager()

    headers = {
        "Content-Type": "application/json",
        "Client-Request-ID": "23040"
    }

    data = json.dumps({
        "model": "qwen2.5-coder:latest",
        "prompt": "What are the consequences of AI?",
        "stream": True
    })

    response = http.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        headers=headers,
        body=data,
        preload_content=False
    )

    for chunk in response.stream():
        chunk_data = chunk.decode('utf-8')
        try:
            json_response = json.loads(chunk_data)
            if 'response' in json_response:
                print(json_response['response'], end='', flush=True)
        except json.JSONDecodeError:
            pass




if __name__ == '__main__':
    TestingStreams1()




def TestingStream1(args):
     http = urllib3.PoolManager()

     headers = {
          "Content-Type": "application/json",
          "Client-Request-ID": "23040"
      }

     data = json.dumps({
        "model": "qwen2.5-coder:latest",
        "prompt": "What are the consequences of AI?",
        "stream": True
    })

     response = http.request(
          method="POST",
          url="http://localhost:11434/api/generate",
          headers=headers,
          body=data,
          preload_content=False
     )
     print(f"{response.status}, {response.headers},\n\n {response.data.decode('utf-8')}")


def TestingStreams2():
    http = urllib3.PoolManager()


    headers = {
        "Content-Type": "application/json",
        "Client-Request-ID": "23040"
    }

    data = json.dumps({
        "model": "qwen2.5-coder:latest",
        "prompt": "What are the consequences of AI?",
        "stream": True
    })

    response = http.request(
        method="POST",
        url="http://localhost:11434/api/generate",
        headers=headers,
        body=data,
        preload_content=False
    )

    for chunk in response.stream():
        chunk_data = chunk.decode('utf-8')
        try:
            json_response = json.loads(chunk_data)
            if 'response' in json_response:
                print(json_response['response'], end='', flush=True)
        except json.JSONDecodeError:
            pass






if __name__ == '__main__':
    TestingStreams1()
