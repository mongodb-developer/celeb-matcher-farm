# Celebrity Matcher (FARM Stack) Demo

You can try out this Celebrity Matcher app at: https://mongodb-celeb-search.com/

This is a small FARM (FastAPI, React, MongoDB) project that illustrates integration with vector search, and AWS's Bedrock model hosting service.

## Run it!

You can run the development version with [Docker Compose].

### Environment Variables

First, you must configure the application, using a `.env` file,
in the root directory of the project. (The one that contains `compose.yml`).

You need to set the following variables:

| Variable           | Description                                                                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **MONGODB_URI**    | The connection string (URI) for a MongoDB Atlas cluster. The connection string must contain the name of the database you want to connect to! |
| **AWS_ACCESS_KEY** | An AWS access key with permission to use the Bedrock service.                                                                                |
| **AWS_SECRET_KEY** | The secret key associated with AWS_ACCESS_KEY.                                                                                               |
| **DEBUG**          | Set this to "true" to enable stack traces and reload. Do **not** enable in production.                                                       |

### Install dependencies
You will need to ensure you install the dependencies for both the frontend and backend applications, using the same images as the docker compose containers.

For the front end, run:

```shell
docker run -it --rm --name nodetest -v .:/opt/app -w /opt/app/frontend node:22 /bin/bash -c "rm -rf ./node_modules && npm install"
```

If you've ever used another version of the Celebrity Matcher (MERN, Go, C#), you may need to force a rebuild of the backend image.

```shell
docker compose up --build --force-recreate
```

### Running the application

Once you've set those, you can spin up the application with:

```shell
docker compose up
```

This will spin up three containers:

| Service      | Port | Description                                                                                                            |
| ------------ | ---- | ---------------------------------------------------------------------------------------------------------------------- |
| **Frontend** | 8002 | A React application, created with [create-react-app], and running in development mode.                                 |
| **Backend**  | 8003 | A FastAPI application that routes requests from frontend to MongoDB & [Amazon Bedrock].                                |
| **Nginx**    | 8001 | A simple reverse-proxy that sits in front of frontend & backend, allowing them to be served from the same host & port. |

Both frontend and backend are configured to load any code changes made on-disk.

## Development

This is a small, stupidly-fast-moving project.
Currently there are no tests (although there should be!),
and no scripts for deployment.
We'll get there!

### Backend

All endpoints in the backend must be beneath the `/api/` path prefix.
That's how Nginx knows to route to the backend, and not the frontend.

[Docker Compose]: https://docs.docker.com/compose/
[create-react-app]: https://create-react-app.dev/docs/getting-started/
[Amazon Bedrock]: https://aws.amazon.com/bedrock/
