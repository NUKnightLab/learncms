# learn.knightlab.com CMS

Learn.knightlab.com is a website created by students, for students, to help develop web making skills.

# Developing the CMS

## Prereqs
If you are going to work on developing the CMS, you need to have installed Python 3 and Postgres 9.x. Then you have to create a virtual environment and initialize the database.

See [SETUP.md](SETUP.md) for details.

In most respects, the CMS is a standard Django application. The object model is meant to be light, because we are trying to leave a lot of flexibility for the content of lessons.
We're using web components to support authoring rich lessons with sophisticated behavior while minimizing the specialist knowledge needed to write a lesson.

Authors do need to understand how to include other pieces of content by reference: the `LessonView` scans the markup in the `Lesson.content` field and, for
specific web components, interprets a `ref` attribute value as the `slug` for a companion `model instance` in the CMS with which to "fill-in" attributes of the component. This ensures content
consistency while leaving flexible how the components can be used.

Otherwise, there's a slightly hackish `GeneralImage` model which provides a way to upload images (or really, any media) so that it can be served to readers of the site. The idea is that once an image
is uploaded, its URL can be copied into the lesson content.

Over time, we hope to make the content authoring provide more tools to manage these relationships, but in our case, we're not interested in hiding the details from our authors, so it's not
the top priority. To be honest, there's more than a whiff of [bad code smell](http://martinfowler.com/bliki/CodeSmell.html) around the `GeneralImage` but it's where we are now.

# Developing Webcomponents

Work on the webcomponents is as simple as running a local webserver in the `components` directory. If you have the python
`virtualenv` installed as described in [SETUP.md](SETUP.md), then it can be as simple as this:

    $ cd components && python -m http.server 8000

Otherwise, the components are meant to be self-documenting. The `index.html` file should be kept up to date if new components are added
or if guidelines need to be set.


# Dependency issues

There is some trickiness sorting out pg and pillow for older Python which we need until
the project is updated to use newer Django.

Mac

```bash
xcode-select --install                           # if not already
brew install libpq
brew install jpeg libtiff little-cms2 openjpeg webp freetype

export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/libpq/lib \
-L/opt/homebrew/opt/jpeg/lib \
-L/opt/homebrew/opt/libtiff/lib \
-L/opt/homebrew/opt/little-cms2/lib \
-L/opt/homebrew/opt/openjpeg/lib \
-L/opt/homebrew/opt/webp/lib \
-L/opt/homebrew/opt/freetype/lib"
export CPPFLAGS="-I/opt/homebrew/opt/libpq/include \
-I/opt/homebrew/opt/jpeg/include \
-I/opt/homebrew/opt/libtiff/include \
-I/opt/homebrew/opt/little-cms2/include \
-I/opt/homebrew/opt/openjpeg/include \
-I/opt/homebrew/opt/webp/include \
-I/opt/homebrew/opt/freetype/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/libpq/lib/pkgconfig"

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```


Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y libpq-dev gcc python3-dev
sudo apt-get install -y build-essential \
  libjpeg-dev zlib1g-dev libtiff5-dev libfreetype6-dev \
  libwebp-dev liblcms2-dev libopenjp2-7-dev

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

