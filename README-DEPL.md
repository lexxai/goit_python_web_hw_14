# DEPLOY to koyeb.com
![deploy](doc/deploy-koyeb-01.png)

![deploy](doc/deploy-koyeb-02.png)

![deploy](doc/deploy-koyeb-03.png)

![deploy](doc/deploy-koyeb-04.png)

![deploy](doc/deploy-koyeb-05.png)

![deploy](doc/deploy-koyeb-06.png)

![deploy](doc/deploy-koyeb-07.png)

![deploy](doc/deploy-koyeb-08.png)

![deploy](doc/deploy-koyeb-09.png)

![deploy](doc/deploy-koyeb-10.png)

![deploy](doc/deploy-koyeb-11.png)

![deploy](doc/deploy-koyeb-12.png)

![deploy](doc/deploy-koyeb-13.png)

## JS CLIENT

![deploy](doc/deploy-koyeb-14.png)

## AUTOMAIC RE-DEPLOOY ON GIT COMMIT 

![deploy](doc/deploy-koyeb-15.png)

### IF AUTOMAIC RE-DEPLOOY ERROR

![deploy](doc/deploy-koyeb-16.png)

## RESULT AFTER AUTH

![deploy](doc/deploy-koyeb-17.png)

## KOYEB CACHED STATIC

![deploy](doc/deploy-koyeb-18.png)

![deploy](doc/deploy-koyeb-19.png)

```
class StaticFilesCache(StaticFiles):
    def __init__(self, *args, cachecontrol="public, max-age=31536000, s-maxage=31536000, immutable", **kwargs):
        self.cachecontrol = cachecontrol
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs) -> Response:
        resp: Response = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cachecontrol)
        return resp


def add_static(_app):
    _app.mount(
        path="/static",
        app=StaticFilesCache(directory=settings.STATIC_DIRECTORY, cachecontrol="private, max-age=3600"),
        name="static",
    )
    _app.mount(path="/sphinx", app=StaticFilesCache(directory=settings.SPHINX_DIRECTORY, html=True), name="sphinx")

```

![deploy](doc/deploy-koyeb-20.png)

## DATABASES
### PG KOYEB

![deploy](doc/deploy-koyeb-db-01.png)

![deploy](doc/deploy-koyeb-db-redis-01.png)

### REDIS redislabs.com
![deploy](doc/deploy-redis-01.png)

![deploy](doc/deploy-redis-02.png)
