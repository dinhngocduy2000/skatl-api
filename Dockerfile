# Stage 1: Build dependencies
FROM python:3.11-alpine AS builder

WORKDIR /app
# Install build dependencies for packages like bcrypt, pandas
RUN apk add --no-cache \
    build-base \
    linux-headers \
    && pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Stage 2: Final image
FROM python:3.11-alpine

WORKDIR /app
# Copy Python packages and binaries
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
# Copy application code
COPY ./app .

ENV PYTHONPATH=":/app"
EXPOSE 8000
CMD ["uvicorn", "cmd.main:app", "--host", "0.0.0.0", "--port", "8000"]