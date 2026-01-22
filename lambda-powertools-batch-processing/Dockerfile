FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY pyproject.toml .

# Install the specified packages
RUN pip install .

# Copy function code
COPY lambda/app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]
