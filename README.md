## Django based backend for paint company project

### Login endpoint


	Endpoint: POST /api/token

	Payload
	{
		"username": <USERNAME>,
		"password": <PASSWORD>
	}

	Response
	{
		"access": <JWT_ACCESS_TOKEN>,
		"refresh": <JWT_REFRESH_TOKEN>
	}

### Get user information


	Endpoint: GET /api/user/me

	Header
	Authorization: Bearer <JWT_ACCESS_TOKEN>

	Response
	{
	    "id": "usr_JXm7dQBq5kYyO",
	    "username": "jane",
	    "is_head_office_staff": false,
	    "can_view_paint_list": true,
	    "can_edit_paint_status": true,
	    "can_edit_paint_inventory": false
	}

### List all paints

	Endpoint: GET /api/paints

	Header
	Authorization: Bearer <JWT_ACCESS_TOKEN>

	Response
	{
	   "data":[
	      {
	         "id":"pnt_DkdrG9MBgbJ8o",
	         "color":"blue",
	         "status":"available",
	         "inventory":3
	      },
	      {
	         "id":"pnt_kBA3GgmMg5n7q",
	         "color":"grey",
	         "status":"running_low",
	         "inventory":2
	      },
	      {
	         "id":"pnt_N1j0kaJlg2Zlz",
	         "color":"white",
	         "status":"out_of_stock",
	         "inventory":0
	      }
	   ],
	   "total":3
	}

### Update paint inventory

	Endpoint: PUT /api/paints/<PAINT_ID>/inventory

	Header
	Authorization: Bearer <JWT_ACCESS_TOKEN>

	Payload
	{
		"inventory": <NEW_PAINT_INVENTORY>
	}

	Response (will return the updated paint information)
	[
	    {
	        "id": "pnt_kBA3GgmMg5n7q",
	        "color": "blue",
	        "status": "out_of_stock",
	        "inventory": 5
	    }
	]

### Update paint status

	Endpoint: PUT /api/paints/<PAINT_ID>/status

	Header
	Authorization: Bearer <JWT_ACCESS_TOKEN>

	Payload
	{
		"status": <NEW_PAINT_STATUS>
	}

	paint status choices: "available", "running_low", "out_of_stock"

	Response (will return the updated paint information)
	[
	    {
	        "id": "pnt_kBA3GgmMg5n7q",
	        "color": "blue",
	        "status": "out_of_stock",
	        "inventory": 5
	    }
	]

