# FROM python:3.11-slim

# WORKDIR /app
# RUN apt-get update && apt-get install -y build-essential
# # Copy the requirements file and install dependencies
# COPY ./skatl-api/requirements.txt /app/requirements.txt
# RUN pip install --upgrade pip \
#     && pip install --no-cache-dir --upgrade -r requirements.txt

# COPY ./skatl-api/app .
# # Expose the port the app will run on
# EXPOSE 8000
# CMD ["uvicorn", "cmd.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

ENV PYTHONPATH=":/app"

EXPOSE 8000
CMD ["uvicorn", "cmd.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]