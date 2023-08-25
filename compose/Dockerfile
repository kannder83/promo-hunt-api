FROM python:3.11
ENV PYTHONUNBUFFERED 1

#Directory work
WORKDIR /usr/src/app

#Copy requirements files
COPY requirements.txt ./

# Install 
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run the additional command
RUN playwright install && playwright install-deps

# Excecute program
CMD python3.11 main.py