#!/usr/bin/env python

import socket
import json
import urllib3

"""The idea is to create a pipeline design to communicate with AI

overview
----------


"""

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
