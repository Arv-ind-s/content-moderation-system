FROM public.ecr.aws/lambda/python:3.11

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
# We use --no-cache-dir to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
# Copy function code
COPY src ${LAMBDA_TASK_ROOT}/src

# Set the CMD to your handler
CMD [ "src.api.main.handler" ]
