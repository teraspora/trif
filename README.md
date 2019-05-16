# Trif

## Overview

Trif is a web application which classifies and offers for sale high-definition prints of abstract fractal images created in Java using a plethora of mathematical functions iterated over the complex plane.

## Specification

The application must store an indeterminate number of images in non-volatile web-accessible storage.

It must provide methods to classify and filter these images based on various characteristics.

In order to do this, it must store or be able to extract data about the functions used to generate an image.   This will be facilitated by these data being encoded in the filenames of the images.

The administrator must be able to add or delete images.

Images must be stored in low resolution (877x620 pixels and 436x310 pixels) but the originals are 14032x9920 pixels, and it is these originals from which high-definition prints (A0, A1, A2, A3) will be made for purchasers.   The filenames of the originals have a one-to-one relationship to the filenames of the low-resolution versions, so orders can be processed without ambiguity.

The application must be able to display the full set of images to the user, suitably scaled in size so as to display a number per viewport, and also let the user select images similar to a given image.   An "Images like this" link should be available for all images, which filters the set by the functions used to generate the images.   Most images have been generated by two functions, usually composed but in some cases alternated, so the user should be able to filter the set by either or both, and by an optional pre-transform.

Advanced functionality should allow the user to filter by other parameters used in the image generation and encoded in the filename, in particular `subc`, `scp` and `sri`.   These are Boolean parameters which when true signify, respectively, that the added constant in the escape-time fractal algorithm has subsequently been subracted, that the same has been done for the pre-transformation function, and that the real and imaginary parts of z have been switched prior to iteration.

In future versions the user should also be able to filter by the predominant colour or quantity of black.   This, however, requires some thinking about as it involves building logic to create histograms and make decisions based on their values, so will not be available in the initial version.

The application must provide secure user registration, authentication and authorisation.   It must provide a secure password reset facility in case of forgotten passwords.   It will not provide a "Forgot my email" facility.

When a user clicks on an image it should be enlarged to roughly 80% of the viewport, and a link to buy should be prominent.

If a user clicks to buy, they should be taken to a page where they can select a size, be informed of the price and complete the transaction with a credit card or Paypal etc.

The application must maintain a "shopping basket" or "cart" so that the user can buy more than one print in a single transaction.   These data should be stored in the database so that if the user does not complete a purchase the items will remain in the basket and be there next time they log in.

A checkout and payment facility must be provided using a trusted third-party library compatible with Django.

In order not to distract or detract from the images themselves, the layout and design of the rendered pages should be as clean and simple as possible.

## Design decisions

- Deployment platform:      Heroku
- Database:                 Postgresql as Heroku add-on
- Image storage:            S3
- Versions:                 Python(3.7.1), Django(2.1.7)
- CI / testing:             Travis
- Payment processing:       Stripe
- Styling:                  Materialize
- Front-end logic           Vue, possibly... or not

### Models

#### User

- Represents a user, who can register with an email address and thereafter be authenticated;
- Fields:  for each user we need name, email, id, whether registered and whether authenticated. We will need to link to the orders table with a foreign key.

#### Image

- Represents a fractal image that can be displayed, that can be ordered as a print, that contains information about the functions and parameters used to create it, and that remembers orders;
- Fields: name, image_id.   We could pre-extract the creation data from the filenames and store as fields, but it will perhaps be simpler, and minimally expensive, to create functions to extract the data as needed. Each Image item must provide a method to get both small and large versions from storage. 

#### Order

- Represents an Order made by a User for an Image;
- Fields: order_id, user_id (foreign key), order_details (containing despatch address, list of Image items and quantities, whether paid).    

### Views and Templates

- `base.html` will contain header and footer with links to register / login.   Other templates will inherit from this:
- `index.html` will be a Home Page displaying some images with links;
- `about.html` will provide information about the application and the developer;
- Other views will enable the user to view the entire set of images (maybe with pagination) or subset based on filtering criteria;
- Clicking on a single image will cause it to be rendered alone, at \~80% screen width, with a "Buy" button at bottom right.
- Other views will enable a user to register, deregister or amend account details.

## Development process log / overview

* Set up S3 and Stripe accounts, created S3 bucket for static files
* Set up basic Django 2 project structure (project: 'trif')
* Created and set environment variables
* S3 and Stripe settings
* Other configuration in settings.py
* Set up on Heroku and connected Github for automatic deployment on push
* Configure Heroku Postgres database; using SQLite locally
* Upload images to S3 bucket: Source Location: "trif-store/static/images/"
* Create app: 'fract' and tested with 'Hello World' page
* Do migrations, create superuser etc.
* Create User model and views following [Corey Schafer's Django 2 tutorials][0], as suggested using code from Bootstrap and CS in base template.   So I will try Bootstrap instead of Materialize
* Create Image model, migrate
* Instantiate a set of Image objects (which simply contain the filename and size, as strings), corresponding to the images actually stored as static assets in my S3 bucket
* Iterate over this set, saving each Image object to the database.   Used local images folder.   See the [console log][1]
* Many issues ensued, initially caused, I think, by my mistaken deletion of a migrations directory. At one point I upgraded Django from 2.1 to 2.2, backed up relevant files, recreated the project and apps.   Later, after mistakenly pushing a faulty commit, I got into a mess with git and ended up doing a `git rebase --hard` and then `git push -f`.   Not a very clean solution, rewriting history etc. but it got me sorted.
* Minor tweaks to styling etc.
* Change home page to a class-based view, subclassing ListView
* Implement random ordering and [pagination][2] using a [custom template tag][3]
* 


[0]: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
[1]: file://shell.log
[2]: https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
[3]: https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/