# N8N Check Links Sample

A project that monitors external links by pinging them and sends Telegram notifications with the status codes using N8N automation platform.

## Overview

This project uses N8N (a workflow automation tool) running in Docker to:
- Monitor external links by sending HTTP requests
- Check response status codes
- Send Telegram notifications with the link status
- Use N8N's built-in Telegram integration

## Features

- **Link Monitoring**: Automatically ping external URLs and check their availability
- **Status Code Reporting**: Monitor HTTP response codes (200, 404, 500, etc.)
- **Telegram Notifications**: Send real-time notifications via Telegram when links are down or status changes
- **Dockerized Setup**: Easy deployment using Docker containers
- **Built-in Integration**: Uses N8N's native Telegram integration

## Prerequisites

- Docker and Docker Compose
- Telegram Bot Token and Chat ID
- List of URLs to monitor

## Components

- **N8N**: Workflow automation platform
- **Docker**: Containerization for easy deployment
- **Telegram Bot**: Built-in N8N integration for messaging
- **Link list**: Configuration file with URLs to monitor

## Usage

1. Configure your links in the `data/links-to-watch.txt` file
2. Set up Telegram Bot Token and Chat ID
3. Deploy the N8N workflow using Docker
4. Monitor link status via Telegram notifications

## Project Structure

```
n8n-check-links-sample/
├── Readme.md
└── data/
    └── links-to-watch.txt    # List of URLs to monitor
```

## Getting Started

1. Add your URLs to monitor in `data/links-to-watch.txt`
2. Configure N8N with your Telegram Bot credentials
3. Set up your workflow to ping links and send notifications
4. Deploy using Docker

This project demonstrates how to create an automated monitoring system that keeps you informed about the health of your external dependencies via Telegram.

