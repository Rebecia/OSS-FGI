# i18next-react-postprocessor

embed React elements inside your i18next translation strings

# About

because sometimes you just want to dump some JSX into your l10n'd text and don't want to be bothered with the whole react-i18next dog-and-pony show.

# Getting Started

```sh
$ npm install --save i18next-react-postprocessor
```

# Usage

import the package in the usual way, and use a new instance of the exported class as i18next middleware:

```javascript
import i18next from 'i18next';
import ReactPostprocessor from 'i18next-react-postprocessor';

i18next
  .use(new ReactPostprocessor())
  .init();
```

then when it's time to render translated strings, make sure you set the `postProcess` option to 'reactPostprocessor':

```javascript
import i18next from 'i18next';
import React from 'react';

function MyComponent(props) {
  return (
    <div>
      {i18next.t(`myKey`, {
        postProcess: `reactPostprocessor`
      })}
    </div>
  );
}
```

or, if you're using it in more than just a few places, it might be worth adding to i18next's init options instead:

```javascript
i18next
  .use(new ReactPostprocessor())
  .init({
    postProcess: [ `reactPostprocessor` ]
  });

// now you don't need to specify "postProcess: 'reactPostprocessor'" when calling i18next.t
```

the postprocessor by default looks for tokens delimited by `<angleyBrackets>` to perform interpolation of React elements:

```javascript
i18next
  .use(new ReactPostprocessor())
  .init({
    lng: `en`,
    postProcess: [ `reactPostprocessor` ],
    resources: {
      en: {
        translation: {
          myKey: `just <clickHere> to do the things`
        }
      },
      fr: {
        translation: {
          myKey: `<clickHere> et voila`
        }
      }
    }
  });
```

element interpolation is done just like regular ol' string interpolation:

```javascript
render() {
  return (
    <div>
      {i18next.t(`myKey`, {
        clickHere: ( <img onClick={() => console.log(`click!`)} src="pug.jpg" /> )
      })}
    </div>
  );
}
```

# API

### ReactPostprocessor({opts})

```javascript
const middleware = new ReactPostprocessor({
  keepUnknownVariables: Boolean
  prefix: String
  suffix: String
});
```

all fields are optional.

`keepUnknownVariables` controls whether or not to preserve any interpolation tokens which aren't present in the options passed to `i18next.t`; it defaults to false (meaning tokens with no corresponding value are replaced with the empty string).  `prefix` and `suffix` define the beginning and end of the interpolation token to look for; they default to '<' and '>' respectively.

# Development & Example App

```sh
$ git clone https://www.github.com/orzechowskid/i18next-react-postprocessor
$ npm install
[ edit edit edit... ]
$ npm run example
$ open http://localhost:8808
[ verify verify verify... ]
$ npm run build
```

# Testing

a full test suite is located in src/\__tests__ .  `npm run test` should run `jest --verbose --coverage`.

# License

MIT
