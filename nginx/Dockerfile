FROM nginx:1.25-alpine

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom configuration
COPY default.conf /etc/nginx/conf.d/

# Security: Run as non-root (nginx already does this in alpine)
# Create directory for static files
RUN mkdir -p /usr/share/nginx/html/static

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1
