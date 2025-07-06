FROM python:3.12-slim

LABEL authors="Aashma Dahal"
ENV RUNNING_IN_DOCKER=true

WORKDIR /app

# Copy pyproject.toml and lock file first for layer caching
COPY pyproject.toml uv.lock ./

# Install uv globally
RUN pip install uv

# Install dependencies into the system environment
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the code
COPY . .

EXPOSE 9000

CMD ["python", "main.py"]