FROM diggspapu/data-science-environment:latest

# Copy the rest of the application's source code to the container
COPY . .

# Expose the port for Jupyter Notebook
EXPOSE 8811

# Command to run Jupyter Notebook and keep the container running
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --port=8811 --no-browser --allow-root && tail -f /dev/null"]
