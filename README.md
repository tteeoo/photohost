![logo](https://photohost.tech/image/dcba46643a66e02d7fa97edd6cfd6c1f2a9ae4629e1b8e592db96fccc0bf1e0b.png)

Free and open source image hosting service.

<hr>

This site is hosted on a custom built home server running nginx, it uses a light weight python web framework called Flask.

Photohost is free to use, with a 32MB upload limit.

Only `.png`, `.jpeg`, `.jpg`, `.gif`, `.svg`, and `.tif` files can be uploaded.

If you'd like to run this on your own, just be sure to change `app.config["UPLOAD_FOLDER"]` to where you'd like the files to be uploaded.

https://photohost.tech

# How it works

When you upload a file, the contents are hashed with sha256. This hash becomes the new filename, and it is saved to the server. 

When a `/image/` path is resolved, the text after the `/` will be treated as a file and be fetched from a seperate uploads folder.

A `/view/` path will fetch the image, but also embed it in html, and tell you the image's URL.

Since you can only upload images, the filenames are changed, and images are fetched from a specific directory, the site (should be) immune to any sort of filesystem injection.

jQuery is used for the image previews when you select an image for uploading.

# License

All files (that make up photohost, *not* uploaded content) are licensed under the MIT License.
