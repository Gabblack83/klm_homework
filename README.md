# KLM HOMEWORK

## Installation
- Clone the [repository](https://github.com/Gabblack83/klm_homework)
- In the cloned local folder issue the following command:

`docker build -t klm_homework:0.0.1 .`
- Once the build is completed issue the following command to start the container:

`docker run -it -p 8080:8001 klm_homework:0.0.1`
- It port-forwards port 8001 of the container to your local 8080 port
- You can access the application on your localhost at port 8080 (http://localhost:8080)

## Deviations from preferred tech stack
I used Vue.js instead of the preferred Angular.js due to being familiar 
with the former and have no previous experience with the latter.

## Additional Data
I added 2 extra datasets to the module to be able to achieve what I had in mind. 

These are both publicly available:
- https://github.com/komsitr/country-centroid/blob/master/country-centroids.csv
- https://gist.github.com/stevewithington/20a69c0b6d2ff846ea5d35e5fc47f26c

I enriched the datasets with continent geographical centroids and 
aligned the country names and codes among the datasets.

Due to the specific requirements of my approach, I only used the portion of the 
original data that had valid longitude and latitude values present. 
I added a short disclaimer about it to the UI.

## Tradeoffs
Due to the limited time I was able to spend on this assignment the following tradeoffs were applied:
- No authentication / authorization
- No meaningful web-security features:
  - secure HTTP headers
  - CSRF protection (only GET calls are present anyway)
  - session management
  - HTTPS
  - etc.
- I used Flask as a quick and easy framework. No production grade WSGI server was added. 
Normally, I would probably use FastAPI and an ASGI server.
- I used pip for installing packages. Normally, I would use something with a lock file, like poetry.
- No component tests in the client side code.
- I built a quasi monolith. Normally I would not consider Python as Vue's server side directly, 
but this way I spared some time by omitting the node.js server side from the middle.
- I used vue-cli for Vue building which is outdated. Normally, I would use vite for this purpose.
- I found no functional bugs in the UI so far, but the UI/UX design and 
functionality could have used a bit more attention.
- Not being previously familiar with any geographic map handling library 
I aimed for a kind of simplistic goal to fit to the given timeframe.