## Easy Challenges

| Challenge Name   | URL                   | Container Port | Notes                     |
|------------------|-----------------------|----------------|---------------------------|
| cookie_monster   | http://localhost:8001 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |
| flagcombined     | http://localhost:8002 | 80             | Runs on port 80 internally (likely a static or PHP-based challenge). |
| treasure_hunt    | http://localhost:8003 | 80             | Runs on port 80 internally (likely a static or PHP-based challenge). |

## Medium Challenges

| Challenge Name     | URL                   | Container Port | Notes                     |
|--------------------|-----------------------|----------------|---------------------------|
| cookie_64          | http://localhost:8011 | 80             | Runs on port 80 internally (likely a PHP-based challenge). |
| echoes_of_machine  | http://localhost:8012 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |
| flagnet            | http://localhost:8013 | 80             | Runs on port 80 internally (likely a PHP-based challenge). |

## Hard Challenges

| Challenge Name     | URL                   | Container Port | Notes                     |
|--------------------|-----------------------|----------------|---------------------------|
| blind_sqli         | http://localhost:8021 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |
| cookie_monsters_inc| http://localhost:8022 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |
| polluted_url       | http://localhost:8023 | 3000           | Runs on port 3000 internally (likely a Node.js-based challenge). |
| ssti               | http://localhost:8024 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |
| xxe                | http://localhost:8025 | 5000           | Runs on port 5000 internally (likely a Python-based challenge). |


## Use

1. Run `docker-compose up --build` to start all services.
2. To stop the services, run `docker-compose down`.
