# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------
import re
import os
from utils.config import Config

URL_PARAMETER_PLACEHOLDER = "{}"


def swagger_resource_path_to_resource_id_template(path):
    path_parts = path.split("?", maxsplit=1)
    url_parts = path_parts[0].split("/")
    idx = 1
    while idx < len(url_parts):
        if idx == 1 and re.match(r'^\{[^{}]*}$', url_parts[idx]):
            # ignore to the parameter name in first part of url, such as `/{parameter}` or `/{parameter}/...`
            # But the placeholder in first part like `/indexes('{indexname}')` will be processed
            idx += 1
            continue
        url_parts[idx] = re.sub(r'\{[^{}]*}', URL_PARAMETER_PLACEHOLDER, url_parts[idx])
        idx += 1
    path_parts[0] = "/".join(url_parts)
    return "?".join(path_parts)


def swagger_resource_path_to_resource_id(path):
    path_parts = path.split("?", maxsplit=1)
    url_parts = path_parts[0].split("/")
    idx = 1
    while idx < len(url_parts):
        if idx == 1 and re.match(r'^\{[^{}]*}$', url_parts[idx]):
            # ignore to the parameter name in first part of url, such as `/{parameter}` or `/{parameter}/...`
            # But the placeholder in first part like `/indexes('{indexname}')` will be processed
            idx += 1
            continue
        # replace all placeholders in part
        url_parts[idx] = re.sub(r'\{[^{}]*}', URL_PARAMETER_PLACEHOLDER, url_parts[idx])
        idx += 1
    path_parts[0] = "/".join(url_parts).lower()
    return "?".join(path_parts)


def resolve_path_to_uri(path):
    relative_path = os.path.relpath(path, start=Config.get_swagger_root()).replace(os.sep, '/')
    if relative_path.startswith('../'):
        raise ValueError(f"Invalid path: {path}")
    if relative_path.startswith('./'):
        relative_path = relative_path[2:]
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    return relative_path
