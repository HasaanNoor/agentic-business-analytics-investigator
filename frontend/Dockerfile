FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_BASE_URL=/api
ARG VITE_DATA_MODE=api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_DATA_MODE=$VITE_DATA_MODE
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=10s --timeout=5s --retries=12 CMD wget -qO- http://127.0.0.1/healthz >/dev/null || exit 1
