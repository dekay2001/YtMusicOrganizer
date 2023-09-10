# YtMusicOrganizer

This library was created to help organize a Youtube Music user's file uploads.

The initial implementation is compatible with Python 10.2.

Right now the only script that exists is the `write_my_uploads.py` which expects that you have 
already generated an `oauth.json` file to authorize your access to the Youtube API.  For information
about generating this file see https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html.

It will produce a file from your uploaded personal libary in the following format format...

```
{
    "songs": [
        {
            "name": "Don't Understand",
            "artist": "Post Malone",
            "album": "AUSTIN",
            "year": null
        },
        {
            "name": "Something Real",
            "artist": "Post Malone",
            "album": "AUSTIN",
            "year": null
        },
        ...
```

Next I will be adding a year lookup that will be populated in the generated file, which I have done as a P.O.C. but I wouldn't say
it is production ready.


## Getting Started

- Clone the repository and create a virtual environment to run.
- Activate the virtual environment and run `pip install -r requirements-dev.txt`
- Run the unit tests continuously with the command `bolt ct`.
- Run a coverage report with `bolt cov`.