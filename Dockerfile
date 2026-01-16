# Runtime stage
FROM nginx:stable-alpine3.23

COPY src/index.html /usr/share/nginx/html/

# Health check to verify nginx is serving content
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1
