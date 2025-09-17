FROM continuumio/miniconda3

# Install tools
RUN apt-get update && apt-get install -y nano unzip curl && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# Create non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy files
COPY --chown=user . $HOME/app

# Install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Prepare artifact dir
RUN mkdir -p $HOME/app/artifacts

# Run MLflow server
CMD mlflow server \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_STORE_URI \
    --host 0.0.0.0 \
    --port 5001
