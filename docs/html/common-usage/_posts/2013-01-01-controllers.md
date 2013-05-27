---
layout: default
tags: [controllers]
title: Controllers
area: Common Usage
---


### <a id="rest"></a>RESTful controllers

Verb | Path | Method | Action
---- | ---- | ------ | ------
GET  | /resource | GET | view resources
POST | /resource | POST | create new resource
GET  | /resource/:id | GET | view resource of id
PUT  | /resource/:id | PUT | update resource of id
DELETE | /resource/:id | DELETE | delete a resource of id


Throwing a NotFoundError, InternalServerError, ApplicationError(message, status_code=123)
