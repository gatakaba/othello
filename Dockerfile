FROM python:3.6
RUN pip install pytest-codestyle
RUN pip install pytest-docstyle
RUN pip install pytest-flakes
RUN pip install pytest-mccabe
RUN pip install pytest-cov
RUN pip install numpy
RUN pip install tabulate
