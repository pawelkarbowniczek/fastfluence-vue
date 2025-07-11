FROM node:18-alpine

WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Ustaw zmienne środowiskowe
ENV VITE_API_BASE_URL=https://api.fastfluence.home.lineofcode.pl

EXPOSE 5173

# Uruchom w trybie development z poprawnym API URL
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]