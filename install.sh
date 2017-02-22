docker build -t netcomp-one:latest .
docker run -d -p 5000:5000 netcomp-one
echo "docker started on http://0.0.0.0:5000/"