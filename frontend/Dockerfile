FROM node:18-alpine

WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# NAPRAWA: Vite potrzebuje index.html w root dla SPA routing
RUN cp public/index.html ./index.html

EXPOSE 5173

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5173/ || exit 1

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]