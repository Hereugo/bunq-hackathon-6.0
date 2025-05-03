FROM --platform=linux/amd64 node:20-alpine AS base

WORKDIR /app

# Install build dependencies for native modules
RUN apk add --no-cache python3 make g++ 

COPY . .
RUN npm install --legacy-peer-deps


ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED 1
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

EXPOSE 3000
