# JSVEE asset URL fix in v0.1.1

The v0.1.0 deployment adapter rewrote vendor JavaScript arguments from
`/lib/jsvee/...` to `/learncpp-demo-cupcake/lib/jsvee/...`. The vendor's stylesheet
and script loaders already concatenate those arguments with the activity page's
base, `/learncpp-demo-cupcake/vendor/cupcake/`. Their explicit string concatenation
does not reset to the origin root when an argument begins with `/`.

The two transformations therefore produced:

```text
/learncpp-demo-cupcake/vendor/cupcake/learncpp-demo-cupcake/lib/jsvee/jsvee.css
```

The 404 handler returned JSON, causing the browser's stylesheet MIME error and
preventing JSVEE initialization. The problem was in the served vendor loader,
not the filesystem layout or Apache path mapping.

## Change

Removed the vendor `/lib/` rewrite from `tools/serve_deployment.py`. The adapter
still rebases the activity HTML's `<base>` and the course host's own URLs.
Vendor JavaScript receives its original `/lib/jsvee/...` arguments, so its own
loader constructs exactly:

```text
/learncpp-demo-cupcake/vendor/cupcake/lib/jsvee/jsvee.css
```

The same change fixes both stylesheets and all three script dependencies:
`jsvee.css`, `jsvee-python.css`, `jquery.min.js`, `JSVEE-min.js` and
`JSVEE-python-min.js`. Relative image references in the CSS resolve beside them.
No files moved, no error responses were relabeled as CSS/JavaScript, and no
fallback aliases were added. Original vendor files and their provenance hashes,
course definitions, and the C++ execution adapter remain unchanged.

## Regression coverage

The original test asserted that a prefixed string appeared in the served bundle
and fetched the root `/lib/` alias directly. It missed the vendor's runtime base
concatenation and incorrectly accepted the broken rewrite.

`tools/check_jsvee_loader.mjs` now extracts and executes the actual served vendor
style-loader method and script-loader function against a small DOM stub using
the actual served `<base>`. It fetches their resulting URLs, requires exactly one
deployment prefix, checks HTTP 200 and CSS/JavaScript MIME types, and fetches CSS
sibling images. It reproduced the exact reported malformed URL against v0.1.0
before the fix. It tests URL construction and delivery, not visual animation.

The Python HTTP deployment test also checks that the vendor loader remains
byte-for-byte unchanged and all five canonical asset URLs have the correct MIME
type. When Node is available, it runs the JavaScript regression too. Node remains
a development-only test dependency; it is not required in the runtime container.
The tests also cover a nested deployment path.

See [DEPLOYMENT.md](DEPLOYMENT.md) for v0.1.1 image loading, the administrator's
confirmed host accommodations, and the browser step-through verification.
