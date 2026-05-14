from typing import NewType

HttpStatus = NewType('HttpStatus', int)

HTTP_200_OK = HttpStatus(200)
HTTP_201_CREATED = HttpStatus(201)
HTTP_202_ACCEPTED = HttpStatus(202)
HTTP_400_BAD_REQUEST = HttpStatus(400)
HTTP_404_NOT_FOUND = HttpStatus(404)
HTTP_422_UNPROCESSABLE = HttpStatus(422)
HTTP_500_INTERNAL = HttpStatus(500)