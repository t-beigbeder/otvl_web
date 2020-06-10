/*!
 * modernizr v3.6.0
 * Build https://modernizr.com/download?-arrow-contains-es6array-es6collections-es6math-es6number-es6object-es6string-generators-promises-setclasses-dontmin
 *
 * Copyright (c)
 *  Faruk Ates
 *  Paul Irish
 *  Alex Sexton
 *  Ryan Seddon
 *  Patrick Kettner
 *  Stu Cox
 *  Richard Herrera

 * MIT License
 */

/*
 * Modernizr tests which native CSS3 and HTML5 features are available in the
 * current UA and makes the results available to you in two ways: as properties on
 * a global `Modernizr` object, and as classes on the `<html>` element. This
 * information allows you to progressively enhance your pages with a granular level
 * of control over the experience.
*/

;(function(window, document, undefined){
  var classes = [];


  var tests = [];


  /**
   *
   * ModernizrProto is the constructor for Modernizr
   *
   * @class
   * @access public
   */

  var ModernizrProto = {
    // The current version, dummy
    _version: '3.6.0',

    // Any settings that don't work as separate modules
    // can go in here as configuration.
    _config: {
      'classPrefix': '',
      'enableClasses': true,
      'enableJSClass': true,
      'usePrefixes': true
    },

    // Queue of tests
    _q: [],

    // Stub these for people who are listening
    on: function(test, cb) {
      // I don't really think people should do this, but we can
      // safe guard it a bit.
      // -- NOTE:: this gets WAY overridden in src/addTest for actual async tests.
      // This is in case people listen to synchronous tests. I would leave it out,
      // but the code to *disallow* sync tests in the real version of this
      // function is actually larger than this.
      var self = this;
      setTimeout(function() {
        cb(self[test]);
      }, 0);
    },

    addTest: function(name, fn, options) {
      tests.push({name: name, fn: fn, options: options});
    },

    addAsyncTest: function(fn) {
      tests.push({name: null, fn: fn});
    }
  };



  // Fake some of Object.create so we can force non test results to be non "own" properties.
  var Modernizr = function() {};
  Modernizr.prototype = ModernizrProto;

  // Leak modernizr globally when you `require` it rather than force it here.
  // Overwrite name so constructor name is nicer :D
  Modernizr = new Modernizr();


/*!
{
  "name": "ES6 Array",
  "property": "es6array",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Array per specification.
*/

  Modernizr.addTest('es6array', !!(Array.prototype &&
    Array.prototype.copyWithin &&
    Array.prototype.fill &&
    Array.prototype.find &&
    Array.prototype.findIndex &&
    Array.prototype.keys &&
    Array.prototype.entries &&
    Array.prototype.values &&
    Array.from &&
    Array.of));

/*!
{
  "name": "ES6 Arrow Functions",
  "property": "arrow",
  "authors": ["Vincent Riemer"],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Arrow Functions per specification.
*/

  Modernizr.addTest('arrow', function() {
    try {
      // eslint-disable-next-line
      eval('()=>{}');
    } catch (e) {
      return false;
    }
    return true;
  });

/*!
{
  "name": "ES6 Collections",
  "property": "es6collections",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim", "weakmap"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Map, Set, WeakMap and WeakSet
*/

  Modernizr.addTest('es6collections', !!(
    window.Map && window.Set && window.WeakMap && window.WeakSet
  ));

/*!
{
  "name": "ES6 Generators",
  "property": "generators",
  "authors": ["Michael Kachanovskyi"],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Generators per specification.
*/

  Modernizr.addTest('generators', function() {
    try {
      new Function('function* test() {}')();
    } catch (e) {
      return false;
    }
    return true;
  });

/*!
{
  "name": "ES6 Math",
  "property": "es6math",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Math per specification.
*/

  Modernizr.addTest('es6math', !!(Math &&
    Math.clz32 &&
    Math.cbrt &&
    Math.imul &&
    Math.sign &&
    Math.log10 &&
    Math.log2 &&
    Math.log1p &&
    Math.expm1 &&
    Math.cosh &&
    Math.sinh &&
    Math.tanh &&
    Math.acosh &&
    Math.asinh &&
    Math.atanh &&
    Math.hypot &&
    Math.trunc &&
    Math.fround));

/*!
{
  "name": "ES6 Number",
  "property": "es6number",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Number per specification.
*/

  Modernizr.addTest('es6number', !!(Number.isFinite &&
    Number.isInteger &&
    Number.isSafeInteger &&
    Number.isNaN &&
    Number.parseInt &&
    Number.parseFloat &&
    Number.isInteger(Number.MAX_SAFE_INTEGER) &&
    Number.isInteger(Number.MIN_SAFE_INTEGER) &&
    Number.isFinite(Number.EPSILON)));

/*!
{
  "name": "ES6 Object",
  "property": "es6object",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Object per specification.
*/

  Modernizr.addTest('es6object', !!(Object.assign &&
    Object.is &&
    Object.setPrototypeOf));

/*!
{
  "name": "ES6 Promises",
  "property": "promises",
  "caniuse": "promises",
  "polyfills": ["es6promises"],
  "authors": ["Krister Kari", "Jake Archibald"],
  "tags": ["es6"],
  "notes": [{
    "name": "The ES6 promises spec",
    "href": "https://github.com/domenic/promises-unwrapping"
  },{
    "name": "Chromium dashboard - ES6 Promises",
    "href": "https://www.chromestatus.com/features/5681726336532480"
  },{
    "name": "JavaScript Promises: There and back again - HTML5 Rocks",
    "href": "http://www.html5rocks.com/en/tutorials/es6/promises/"
  }]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 Promises per specification.
*/

  Modernizr.addTest('promises', function() {
    return 'Promise' in window &&
    // Some of these methods are missing from
    // Firefox/Chrome experimental implementations
    'resolve' in window.Promise &&
    'reject' in window.Promise &&
    'all' in window.Promise &&
    'race' in window.Promise &&
    // Older version of the spec had a resolver object
    // as the arg rather than a function
    (function() {
      var resolve;
      new window.Promise(function(r) { resolve = r; });
      return typeof resolve === 'function';
    }());
  });

/*!
{
  "name": "ES6 String",
  "property": "es6string",
  "notes": [{
    "name": "unofficial ECMAScript 6 draft specification",
    "href": "https://people.mozilla.org/~jorendorff/es6-draft.html"
  }],
  "polyfills": ["es6shim"],
  "authors": ["Ron Waldon (@jokeyrhyme)"],
  "warnings": ["ECMAScript 6 is still a only a draft, so this detect may not match the final specification or implementations."],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 String per specification.
*/

  Modernizr.addTest('es6string', !!(String.fromCodePoint &&
    String.raw &&
    String.prototype.codePointAt &&
    String.prototype.repeat &&
    String.prototype.startsWith &&
    String.prototype.endsWith &&
    String.prototype.includes));


  /**
   * is returns a boolean if the typeof an obj is exactly type.
   *
   * @access private
   * @function is
   * @param {*} obj - A thing we want to check the type of
   * @param {string} type - A string to compare the typeof against
   * @returns {boolean}
   */

  function is(obj, type) {
    return typeof obj === type;
  }
  ;

  /**
   * Run through all tests and detect their support in the current UA.
   *
   * @access private
   */

  function testRunner() {
    var featureNames;
    var feature;
    var aliasIdx;
    var result;
    var nameIdx;
    var featureName;
    var featureNameSplit;

    for (var featureIdx in tests) {
      if (tests.hasOwnProperty(featureIdx)) {
        featureNames = [];
        feature = tests[featureIdx];
        // run the test, throw the return value into the Modernizr,
        // then based on that boolean, define an appropriate className
        // and push it into an array of classes we'll join later.
        //
        // If there is no name, it's an 'async' test that is run,
        // but not directly added to the object. That should
        // be done with a post-run addTest call.
        if (feature.name) {
          featureNames.push(feature.name.toLowerCase());

          if (feature.options && feature.options.aliases && feature.options.aliases.length) {
            // Add all the aliases into the names list
            for (aliasIdx = 0; aliasIdx < feature.options.aliases.length; aliasIdx++) {
              featureNames.push(feature.options.aliases[aliasIdx].toLowerCase());
            }
          }
        }

        // Run the test, or use the raw value if it's not a function
        result = is(feature.fn, 'function') ? feature.fn() : feature.fn;


        // Set each of the names on the Modernizr object
        for (nameIdx = 0; nameIdx < featureNames.length; nameIdx++) {
          featureName = featureNames[nameIdx];
          // Support dot properties as sub tests. We don't do checking to make sure
          // that the implied parent tests have been added. You must call them in
          // order (either in the test, or make the parent test a dependency).
          //
          // Cap it to TWO to make the logic simple and because who needs that kind of subtesting
          // hashtag famous last words
          featureNameSplit = featureName.split('.');

          if (featureNameSplit.length === 1) {
            Modernizr[featureNameSplit[0]] = result;
          } else {
            // cast to a Boolean, if not one already
            if (Modernizr[featureNameSplit[0]] && !(Modernizr[featureNameSplit[0]] instanceof Boolean)) {
              Modernizr[featureNameSplit[0]] = new Boolean(Modernizr[featureNameSplit[0]]);
            }

            Modernizr[featureNameSplit[0]][featureNameSplit[1]] = result;
          }

          classes.push((result ? '' : 'no-') + featureNameSplit.join('-'));
        }
      }
    }
  }
  ;
/*!
{
  "name": "ES5 String.prototype.contains",
  "property": "contains",
  "authors": ["Robert Kowalski"],
  "tags": ["es6"]
}
!*/
/* DOC
Check if browser implements ECMAScript 6 `String.prototype.contains` per specification.
*/

  Modernizr.addTest('contains', is(String.prototype.contains, 'function'));


  /**
   * docElement is a convenience wrapper to grab the root element of the document
   *
   * @access private
   * @returns {HTMLElement|SVGElement} The root element of the document
   */

  var docElement = document.documentElement;


  /**
   * A convenience helper to check if the document we are running in is an SVG document
   *
   * @access private
   * @returns {boolean}
   */

  var isSVG = docElement.nodeName.toLowerCase() === 'svg';


  /**
   * setClasses takes an array of class names and adds them to the root element
   *
   * @access private
   * @function setClasses
   * @param {string[]} classes - Array of class names
   */

  // Pass in an and array of class names, e.g.:
  //  ['no-webp', 'borderradius', ...]
  function setClasses(classes) {
    var className = docElement.className;
    var classPrefix = Modernizr._config.classPrefix || '';

    if (isSVG) {
      className = className.baseVal;
    }

    // Change `no-js` to `js` (independently of the `enableClasses` option)
    // Handle classPrefix on this too
    if (Modernizr._config.enableJSClass) {
      var reJS = new RegExp('(^|\\s)' + classPrefix + 'no-js(\\s|$)');
      className = className.replace(reJS, '$1' + classPrefix + 'js$2');
    }

    if (Modernizr._config.enableClasses) {
      // Add the new classes
      className += ' ' + classPrefix + classes.join(' ' + classPrefix);
      if (isSVG) {
        docElement.className.baseVal = className;
      } else {
        docElement.className = className;
      }
    }

  }

  ;

  // Run each test
  testRunner();

  // Remove the "no-js" class if it exists
  setClasses(classes);

  delete ModernizrProto.addTest;
  delete ModernizrProto.addAsyncTest;

  // Run the things that are supposed to run after the tests
  for (var i = 0; i < Modernizr._q.length; i++) {
    Modernizr._q[i]();
  }

  // Leak Modernizr namespace
  window.Modernizr = Modernizr;


;

})(window, document);
