# gmailnotify
Simple GMail new message notifications through Atom feed and libnotify.

## Getting Started

Install dependencies:

```shell
$ pip install --user requests beautifulsoup4 notify2
```

Now, you need to create a config.
Just copy `config.py.example` to `config.py` and fill in your email and app password.

Then it's ready to use:

```shell
$ python3 main.py
```
