CREATE_BOOKING_RESPONSE_SCHEMA = {
  "type": "object",
   "required": ["bookingid", "booking"],
  "additionalProperties": False,
  "properties": {
    "bookingid": {
      "type": "integer",
      "description": "Уникальный идентификатор бронирования"
    },
    "booking": {
      "type": "object",
      "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates"
      ],
      "additionalProperties": False,
      "properties": {
        "firstname": {
          "type": "string"
        },
        "lastname": {
          "type": "string"
        },
        "totalprice": {
          "type": "integer"
        },
        "depositpaid": {
          "type": "boolean"
        },
        "bookingdates": {
          "type": "object",
          "required": ["checkin", "checkout"],
          "additionalProperties": False,
          "properties": {
            "checkin": {
              "type": "string",
              "format": "date",
              "description": "Дата заселения в формате YYYY-MM-DD"
            },
            "checkout": {
              "type": "string",
              "format": "date",
              "description": "Дата выезда в формате YYYY-MM-DD"
            }
          }
        },
        "additionalneeds": {
          "type": "string"
        }
      }
    }
  }
}