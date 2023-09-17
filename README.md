# A simple Poker planning application

## tldr:
`docker compose up`
go to `http://localhost:8080`

## What it is:
A simple pocker planning application fetching a list of Jiras and allowing multiple people to submit their votes.  
backend is a python FastApi container saving plannification data in a sqlite.  
front end is a VueJS application.  

Anybody can go create a session filling the jira host and jql to fetch the stories.
Once created a link/invite_code can be sent to participants.
Each participants can contribute "anonymously" to the plan revealing the final score only when all votes have been cast.

## Documentation:

### Api
Api swagger documentation is available in `http//localhost:8081/docs` once the project has been started

## Contributions:
Contributions are welcome, please follow the standard Open source process

### Linting:
please follow
* pycodestyles standard for the api.
* semistandard standard for the application.

### Tests:
to be added

## License:
Project under GPL License, See LICENSE

## Ressources:
color pannel:
* green: `#0c8579`
* red: `#9e2416`

## Notes:
* anonymously: user_id being returned in the Api responses, it could be possible for the admin to have information on the voters if he really wanted to by checking the requests traffic.