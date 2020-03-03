![logo](https://photohost.tech/image/dcba46643a66e02d7fa97edd6cfd6c1f2a9ae4629e1b8e592db96fccc0bf1e0b.png)

Free and open source image hosting service.

<hr>

This site is hosted on a custom built home server running nginx, it uses a light weight python web framework called Flask.

Photohost is free to use, with a 32MB upload limit.

Only `.png`, `.jpeg`, `.jpg`, `.gif`, `.svg`, `ico`, and `.tif` files can be uploaded.

To upload multiple files, submit a `.zip` with only image files in the root

https://photohost.tech

# How it works

When you upload a file, the contents are hashed with sha256. This hash becomes the new filename, and it is saved to the server. 

When a `/image/` path is resolved, the text after the `/` will be treated as a file and be fetched from a seperate uploads folder.

A `/view/` path will fetch the image, but also embed it in html, and tell you the image's URL.

Since you can only upload images, the filenames are changed, and images are fetched from a specific directory, the site (should be) immune to any sort of filesystem injection.

With multi-file uploads it's a similair story, but the `.zip` is hashed and saved on the server as a folder with the images inside of it. The `/multi/` path is essentially the same as `view`, but can show multiple images.

jQuery is used for the image previews when you select an image for uploading.

# Running on your own

If you wish to run your own instance of photohost, you need some sort of wsgi-compatible web server. Apache has a built in module for dealing with wsgi, but I prefer nginx. If you are using nginx, you will need to proxy it into gunicorn. Gunicorn is a wsgi web server, but it is not as smart or effecient as nginx. Look up a tutorial for how to do this.

Be sure to change `app.config["UPLOAD_FOLDER"]` to where you'd like the files to be uploaded.

# License

All files (that make up photohost, *not* uploaded content) are licensed under the MIT License.
