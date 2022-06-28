### Preliminary notes

The goal of this technical exercise is to fetch Pokémon data from [pokeapi.co](https://pokeapi.co/),
discover new Pokémon and update the existing ones.

Before we dive into code, please allow me to briefly introduce the code structure.

First, I used my own repo for this exercise, this is entirely because I would like the
development environment allowing me to run tests very efficiently.

Second, this repo has three main layers, they help separate the concerns.

Three layers are:

- `src/pokemon/data`: all models and relevant data logic,
- `src/pokemon/interfaces`: interfaces are conceptually the entry points of the systems, they could be an API endpoint, a management command or a webhook etc.
- `src/pokemon/domain`: this is where the business logic resides.

The interface layer provides different means to interact with our system, they are not directly interacting with the data layer. Instead, they are responsible for validating input, calling the domain layers (to do the actual work) and returning output to the clients.


### Get started

1 - Install [Docker](https://docs.docker.com/docker-for-mac/install/).

2 - Go to the project root directory (on a terminal such as iterm2).

3 - Build images and start them using `make build-dev-image`.

4 - Prepare the database, use `make db-migrate` to run the migrations.

5 - Get into the container by doing `make start-shell`, and now run a management command `./manage.py sync_pokemon` command to crawl Pokémon data.
It's likely to take a while to crawl all data, so we can do `./manage.py sync_pokemon 100` to crawl 100 Pokémon data entries, which is much quicker.
We can repeatedly run this management command without creating duplicated Pokémon because it is idempotent.

6 - Kill the current session (e.g. `^ + D` on Mac). Now, we start service `make start-service`. Depending on your current Docker network config, you might experience a Docker error saying pool overlaps with other addresses. If this is the case, do `docker network prune`.

7 - Navigate to `http://0.0.0.0:8090/api/v1/monsters/` on a browser, you will see a list of data entries.

8 - We can run all tests by doing `make run-test`. This should show all test results and the test coverage.
