FROM node:20 AS builder
WORKDIR /front
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY frontend/ .
RUN pnpm run build        # → /front/dist

FROM nginx:1.27-alpine
COPY --from=builder /front/dist /usr/share/nginx/html

