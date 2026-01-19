# `imperial-painter`

A way of generating prototype cards for testing tabletop games!

Creates printable HTML pages using Django and Less/CSS.

Named for the Magic deck, [Imperial Painter](http://www.mtgtop8.com/event?e=6724&d=238610).

## Running the app

To install `imperial-painter`, use the same steps you would for a normal Django project:

* Ensure Postgres is running ([instructions are here](https://www.postgresql.org/) if you need to set it up).
* Use `make install` to create a database in Postgres, create a Python virtual environment, and install dependencies.
* Launch the application using `make run`.

Go to `localhost:8000` in your browser. You'll see a list of generators for different games, and can click through any of them to select a file on your file system. Hitting Generate after that will produce the cards, and you can print them from your browser. Each printed page will contain a 3x3 grid of cards, sized to match standard Magic cards/sleeves; I recommed cutting them out and sliding them into sleeves over the top of existing spares/tokens to produce your prototypes.

## Spreadsheet API

Imperial Painter imports card data from `.xlsx` files.

The contents vary based on the importer and the needs of the particular generator being used. The base `import_cards` (used for most generators) expects a single table, filling an entire sheet, with the following columns:

* `Name` - the name of a card. Uniqueness of names is not enforced.
* `Template` - the name of a Django template file, without the `.html` or the file path leading up to it. For instance, a `Template` entry of `base` for a generator called `my_generator` would resolve to `templates/painter/[my_generator]/base.html`.
    * You can include multiple template names this way, comma-separated - e.g. `character,items`.
    * Any whitespace around template names is removed.
* `Quantity` - optional. This allows you to print a card multiple times.
* Any other columns you wish. These will be converted into variables (see the "Django template API" section).
    * The first blank column header will be taken as the end of the sheet, so your table must be contiguous.
    * Any column name preceded by an asterisk (`*`) will be treated as a _list_ variable. List entries are separated by newlines (Alt+Enter in Excel, and I think Ctrl+Enter in LibreOffice).

Multiple files can be input, and each file can have any number of sheets.

As an example, see [painter/tests/example_cards.xlsx](https://github.com/adam-thomas/imperial-painter/blob/master/painter/tests/example_cards.xlsx). This file is compatible with the `Test Cards` generator, if you want to see it in action.

## Adding custom generators

There are several components to Painter's API. To make a new generator, you need to:

* Create one or more Excel files (`.xlsx`) that contain your card data. This should follow a specific format expected by the importer.
* Decide on a generator name, and add it to the `GENERATORS` dictionary in `settings.py`.
* Create a Django templates folder under `painter/templates/painter/[generator]/`.
    * Add any Django template files you need here. Their names can be arbitrary (see below).
    * Additionally, add a `fonts.html` template. This can be empty, but is also a place where you can add any HTML headers that import fonts. Painter is set up expecting to use Google Fonts, but any other similar system works.
* Create a styling folder at `painter/static/styles/[generator]/`. This expects [Less files](http://lesscss.org/).
    * Add a `custom.less` file to this folder as your entry point, plus any number of other Less files. Any other files should be `@import`ed into `custom.less`.
    * If you don't want to use Less, you can write normal CSS in your `custom.less` file.
* If you need other static assets, add them to the `static` folder somewhere sensible and import them directly in your Django templates. I've conventionally used `static/images/[generator]/` as a location for images.

The other generators can provide examples of the structure and things to copy-and-paste if you need.

### Less/CSS API

Add a `styles/custom.less` file to a static files directory.

The contents of each card are wrapped in a `<div class="template-[template name] full-card">`. All of your styles should be applied within that class.

For fixed sizes, use `rem` instead of `px` or any other measurement. Painter sets a base `font-size` of `1px` across the page, so your `rem` sizes will normally equal the pixel count you want.

Less allows you to import other Less files, so you can split your styles across multiple files if you need despite the singular entry point. If you're unfamiliar with Less, raw CSS is perfectly valid Less, so you can use that too (just make sure the file is still named `custom.less`).

### Django template API

Your templates should contain only the contents of each card. This will be `{% include %}`d into the page template, directly within the `<div class="full-card">` from the previous section.

Within the template, the parameters on each card are available as Django template variables:

* Name: `{{ name }}`
* Template: Unavailable
* Quantity: Unavailable
* Other columns: `{{ c.column_name }}`

Column headings are converted to variable names as follows:

* The name is converted to lowercase.
* Spaces are replaced with underscores.
* Characters other than alphanumerics and underscores are stripped out.

This makes a column called `Rules Text (Full)` into `rules_text_full`, which is then available in the template as `{{ c.rules_text_full }}`.
