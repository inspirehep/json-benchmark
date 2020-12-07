# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# inspirehep is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

FROM python:3.8-slim

WORKDIR /opt/src/
ENTRYPOINT [ "python3" ]
CMD [ "tests.py" ]

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
