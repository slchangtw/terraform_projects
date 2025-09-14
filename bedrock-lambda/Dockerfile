FROM public.ecr.aws/lambda/python:3.12 AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml uv.lock ./

# Install dependencies 
RUN uv sync --no-dev

# Copy the source code
COPY lambda/ ./lambda/

FROM public.ecr.aws/lambda/python:3.12

# Copy the virtual environment contents to Lambda task root (/var/task)
COPY --from=builder /app/.venv/lib/python3.12/site-packages/ /var/task/

# Copy the source code
COPY --from=builder /app/lambda/ /var/task/

CMD ["app.lambda_handler"]