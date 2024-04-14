# md5-es
FASTEST Cryptographic hash library producing a 128-bit (16-byte) hash value

[![npm](https://img.shields.io/npm/v/md5-es.svg?maxAge=2592000)](https://www.npmjs.com/package/md5-es) [![Dependency Status](https://api.travis-ci.org/logotype/es-crypto.svg?path=packages/md5-es)](https://travis-ci.org/logotype/es-crypto?path=packages/md5-es)

node
----

Import `MD5` and call `.hash()` with a string:

```javascript
import MD5 from 'md5-es';
const hash = MD5.hash('tr1z');
console.log(hash);
```

Example output:

```bash
6d86ca3c74636711371637c2d73ec3e48dd1737a
```

Copyright and license
---------------------

Copyright © 2017 logotype

Author: Victor Norgren

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:  The above copyright
notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.