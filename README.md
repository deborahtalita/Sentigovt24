# Sentigovt24

## Installation
### Tailwind Installation:
1. Make sure Node.js and NPM are installed on your system. You can download it from https://nodejs.org/en/download/ and follow the instructions.
2. Install Django Composer (python -m pip install django-compressor).
3. Add compressor to the installed apps inside the settings.py file.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',  # new
]
```
4. Configure the compressor inside the settings.py file.
```python
COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)
```
5. Create two new folders and an input.css file inside the static/css/ folder.
```bash
static
└── css
    └── input.css
```
6. Install Tailwind (npm install -D tailwindcss).
7. Using the Tailwind CLI create a new tailwind.config.js file (npx tailwindcss init).
8. Configure the template paths using the content value inside the Tailwind configuration file.
```javascript
module.exports = {
  content: [
      './**/*.{html,js}'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```
9. Import the Tailwind CSS directives inside the input.css file.
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
10. Add in package.json file.
```json
"scripts": {
    "dev": "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  },
```
11. Run the following command to watch for changes and compile the Tailwind CSS code (npm run dev)
### Running Application
`py manage.py runserver`

### Sweet Alert 2 Installation:
1. Install Sweet Alert 2 (npm install sweetalert2).



