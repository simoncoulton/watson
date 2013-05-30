---
layout: code
tags: [mvc, exceptions]
title: Exceptions
area: Reference Library
package: watson.mvc
module: watson.mvc.exceptions
api: [ApplicationError, NotFoundError, InternalServerError, ExceptionHandler]
---

### ApplicationError

> A general purpose application error.

ApplicationError exceptions are used to redirect the user to relevant http status error pages. Status codes will be looked up against watson.http.STATUS_CODES

#### Attributes

##### status_code

The http response status code association with the error. Defaults to 500.

#### Methods

##### __init__(message, status_code=None)

###### Arguments

Type | Name | Description
-------- | -------- | -----------
string | message | The exception message
int | status_code | The http response status code

--------

### NotFoundError

> 404 Not Found exception.

Extends the ApplicationError exception.

--------

### InternalServerError

> 500 Internal Server Error exception.
