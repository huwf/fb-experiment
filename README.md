# FB Application

To run using Docker on port 80:

	git clone https://github.com/huwf/fb-experiment.git
	cd fb-application
	docker pull huwf/fb-flask-app
	docker run -dt -p 80:80 flask-app

This ADDs the `app` directory to `/app`. For development, it may be better to mount that directory instead.
From the `fb-application` directory, instead use the following to run:
	
	docker run -dt -p 80:80 -v $(pwd)/app:/app flask-app

This has the application running in detached mode. Try `run -it --rm` if you want to view the logs as you work,
 and want to restart it. Alternatively, you can run in detached mode and use `docker logs <<container name>>`.

Most likely, you'll want to run it with the database, so run `docker-compose up -d`.

Obviously we need to change the passwords for any public facing server.

It is probably possible to run on the metal with just Python, or on a different port but I haven't got it to work yet.



