# Use Rocky Linux as the base image
FROM rockylinux:9

# Metadata
LABEL version="1.0"
LABEL maintainer="suryatheking5784@gmail.com"

# Install dependencies (including EPEL and Nginx) EPEL = Extra Packages for Enterprise Linux
RUN yum install -y epel-release && \
    yum install -y nginx && \
    yum clean all


# Expose HTTP port
EXPOSE 80

# Start nginx in the foreground when the container runs
CMD ["nginx", "-g", "daemon off;"]