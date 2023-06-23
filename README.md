# Get IP bot

## Installation

### From source

Build it intuitively (I'm too lazy to describe how to)

### Docker

1. Set environment variables `BOT_TOKEN` and `ADMINS`
    ```bash
    BOT_TOKEN=1234567890:12345678901234567890123456789012345
    ADMINS=1234567890:1234567890:1234567890  # telegram id's of user
    ```
2. From the root of the project run
    ```bash
    docker build -t ip-bot --build-arg BOT_TOKEN=$BOT_TOKEN --build-arg ADMINS=$ADMINS .
    ```
3. To run container
    ```bash
    docker run -d ip-bot
    ```
4. Stop with
    ```bash
    docker kill <container-name/container-id>
    # or
    docker stop <container-name/container-id>
    ```