# syntax=docker/dockerfile:1
FROM varnish:7.6

LABEL maintainer="kitconcept GmbH <info@kitconcept.com>" \
      org.label-schema.name="collective.blog-varnish" \
      org.label-schema.description="collective.blog Varnish image." \
      org.label-schema.vendor="kitconcept GmbH"

COPY etc/varnish.vcl /etc/varnish/default.vcl
