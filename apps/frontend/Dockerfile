# apps/frontend/Dockerfile
FROM node:18-slim
WORKDIR /app
COPY package.json .
RUN npm install --production
COPY src ./src
ENV PORT=8080
EXPOSE 8080
CMD ["node", "src/index.js"]
