FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Optional: expose port if needed
# EXPOSE 8000

# Run the bot
CMD ["python", "bot.py"]
