# First stage: Build environment
FROM node:18.13.0-alpine as builder

# Install Python and essential build tools
RUN apk add --update --no-cache python3 make g++ && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Create a Python virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Create the directory where our app will live
RUN mkdir -p /app
WORKDIR /app

# Copy package.json and yarn.lock to the working directory
COPY package*.json yarn.lock ./

# Install Node.js dependencies
RUN yarn install --network-timeout 1000000

# Copy the rest of the Next.js folder into /app
COPY . .

# Build the Next.js application
RUN yarn build

# Second stage: Runtime environment
FROM node:18.13.0-alpine

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy built assets from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Ensure port 3000 is accessible to our system
EXPOSE 3000

# Run yarn start, as we would via the command line
CMD ["yarn", "start"]
