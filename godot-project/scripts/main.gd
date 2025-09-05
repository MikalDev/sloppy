extends Node2D

@onready var player = $Player
@onready var http = HTTPRequest.new()

var trail_images = []
var move_speed = 200.0
var trail_distance = 100.0
var last_trail_position = Vector2.ZERO
var is_requesting = false
var test_mode = true

func _ready():
	add_child(http)
	http.request_completed.connect(_on_art_received)
	http.timeout = 120.0  # 2 minutes timeout
	last_trail_position = player.position
	print("[READY] AI Art Game Ready!")
	print("Press SPACE to generate random art")
	print("Use arrow keys to move player")
	# Auto-generate test art for comparison
	get_tree().create_timer(1.0).timeout.connect(test_server_connection)
	get_tree().create_timer(3.0).timeout.connect(generate_test_art)

func _process(delta):
	if test_mode:
		handle_test_input()
	else:
		handle_player_movement(delta)
		check_trail_generation()

func handle_test_input():
	if Input.is_action_just_pressed("ui_accept"):  # Space bar
		generate_test_art()

func handle_player_movement(delta):
	var direction = Vector2.ZERO
	if Input.is_action_pressed("ui_right"):
		direction.x += 1
	if Input.is_action_pressed("ui_left"):
		direction.x -= 1
	if Input.is_action_pressed("ui_down"):
		direction.y += 1
	if Input.is_action_pressed("ui_up"):
		direction.y -= 1
	
	if direction != Vector2.ZERO:
		player.velocity = direction.normalized() * move_speed
		player.move_and_slide()

func check_trail_generation():
	if player.position.distance_to(last_trail_position) >= trail_distance:
		generate_trail_art()
		last_trail_position = player.position

func generate_test_art():
	if is_requesting:
		print("[BUSY] Already generating, please wait...")
		return
	
	is_requesting = true
	var prompts = ["flower", "gem", "star", "crystal", "mushroom", "potion", "sword", "shield"]
	var random_prompt = prompts[randi() % prompts.size()]
	var json_data = JSON.stringify({
		"prompt": random_prompt, 
		"width": 512,
		"height": 512,
		"steps": 8,
	})
	var headers = ["Content-Type: application/json"]
	print("[GENERATE] ", random_prompt, " (512x512, 8 steps)...")
	print("[PAYLOAD] ", json_data)
	http.request("http://127.0.0.1:8080/generate", headers, HTTPClient.METHOD_POST, json_data)

func generate_trail_art():
	if is_requesting:
		return
	
	is_requesting = true
	var prompts = ["pixel art flower", "pixel art gem", "pixel art star", "pixel art crystal"]
	var random_prompt = prompts[randi() % prompts.size()]
	var json_data = JSON.stringify({
		"prompt": random_prompt, 
		"width": 512,
		"height": 512,
		"steps": 8,
	})
	var headers = ["Content-Type: application/json"]
	print("[TRAIL] Payload: ", json_data)
	http.request("http://127.0.0.1:8080/generate", headers, HTTPClient.METHOD_POST, json_data)

func _on_art_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
	print("[HTTP RESULT] Result: ", result, " Response Code: ", response_code, " Body size: ", body.size(), " bytes")
	
	# Check for HTTPRequest errors first
	match result:
		HTTPRequest.RESULT_SUCCESS:
			print("[SUCCESS] Request completed successfully")
		HTTPRequest.RESULT_CHUNKED_BODY_SIZE_MISMATCH:
			print("[ERROR] Chunked body size mismatch")
		HTTPRequest.RESULT_CANT_CONNECT:
			print("[ERROR] Cannot connect to server")
		HTTPRequest.RESULT_CANT_RESOLVE:
			print("[ERROR] Cannot resolve hostname")
		HTTPRequest.RESULT_CONNECTION_ERROR:
			print("[ERROR] Connection error")
		HTTPRequest.RESULT_TLS_HANDSHAKE_ERROR:
			print("[ERROR] TLS handshake error")
		HTTPRequest.RESULT_NO_RESPONSE:
			print("[ERROR] No response from server")
		HTTPRequest.RESULT_BODY_SIZE_LIMIT_EXCEEDED:
			print("[ERROR] Body size limit exceeded")
		HTTPRequest.RESULT_BODY_DECOMPRESS_FAILED:
			print("[ERROR] Body decompression failed")
		HTTPRequest.RESULT_REQUEST_FAILED:
			print("[ERROR] Request failed")
		HTTPRequest.RESULT_DOWNLOAD_FILE_CANT_OPEN:
			print("[ERROR] Download file cannot open")
		HTTPRequest.RESULT_DOWNLOAD_FILE_WRITE_ERROR:
			print("[ERROR] Download file write error")
		HTTPRequest.RESULT_REDIRECT_LIMIT_REACHED:
			print("[ERROR] Redirect limit reached")
		HTTPRequest.RESULT_TIMEOUT:
			print("[ERROR] Request timed out")
		_:
			print("[ERROR] Unknown result code: ", result)
	
	is_requesting = false
	
	if result == HTTPRequest.RESULT_SUCCESS and response_code == 200:
		print("[HTTP 200] Parsing JSON...")
		var json = JSON.new()
		if json.parse(body.get_string_from_utf8()) == OK:
			print("[JSON OK] Parsed successfully")
			var data = json.data
			if data.has("success") and data.success and data.has("image"):
				print("[IMAGE] Creating sprite...")
				create_trail_sprite(data.image)
				print("[COMPLETE] Sprite created")
			else:
				print("[AI ERROR] ", data)
		else:
			print("[JSON ERROR] Parse failed")
	elif result == HTTPRequest.RESULT_SUCCESS:
		print("[HTTP ERROR] Code: ", response_code, " Body: ", body.get_string_from_utf8())
	else:
		print("[REQUEST FAILED] Result: ", result, " Code: ", response_code)

func test_server_connection():
	print("[HEALTH] Testing basic server connectivity...")
	var health_http = HTTPRequest.new()
	add_child(health_http)
	health_http.request_completed.connect(_on_health_received)
	health_http.timeout = 10.0  # Short timeout for health check
	var headers = ["User-Agent: Godot-Health-Check"]
	print("[HEALTH] GET request to http://127.0.0.1:8080/health")
	health_http.request("http://127.0.0.1:8080/health", headers, HTTPClient.METHOD_GET)

func _on_health_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
	print("[HEALTH RESULT] Result: ", result, " Response Code: ", response_code, " Body size: ", body.size(), " bytes")
	
	match result:
		HTTPRequest.RESULT_SUCCESS:
			print("[HEALTH SUCCESS] Request completed successfully")
		HTTPRequest.RESULT_CANT_CONNECT:
			print("[HEALTH ERROR] Cannot connect to server")
		HTTPRequest.RESULT_CANT_RESOLVE:
			print("[HEALTH ERROR] Cannot resolve hostname")
		HTTPRequest.RESULT_CONNECTION_ERROR:
			print("[HEALTH ERROR] Connection error")
		HTTPRequest.RESULT_TIMEOUT:
			print("[HEALTH ERROR] Request timed out")
		_:
			print("[HEALTH ERROR] Unknown result code: ", result)
	
	if result == HTTPRequest.RESULT_SUCCESS and response_code == 200:
		print("[HEALTH OK] Server is responding! Body: ", body.get_string_from_utf8())
	elif result == HTTPRequest.RESULT_SUCCESS:
		print("[HEALTH HTTP ERROR] Code: ", response_code, " Body: ", body.get_string_from_utf8())
	else:
		print("[HEALTH FAILED] Result: ", result, " Code: ", response_code)

func create_trail_sprite(image_base64: String):
	print("[IMAGE] Processing base64 image data (", image_base64.length(), " chars)...")
	var image_data = Marshalls.base64_to_raw(image_base64)
	print("[DECODE] Base64 decoded to ", image_data.size(), " bytes")
	var image = Image.new()
	print("[PNG] Loading PNG from buffer...")
	image.load_png_from_buffer(image_data)
	print("[TEXTURE] Creating texture...")
	var texture = ImageTexture.create_from_image(image)
	print("[SPRITE] Creating sprite...")
	var trail_sprite = Sprite2D.new()
	trail_sprite.texture = texture
	
	if test_mode:
		# Random position on screen for test mode
		var screen_size = get_viewport().get_visible_rect().size
		var random_x = randf_range(100, screen_size.x - 100)
		var random_y = randf_range(100, screen_size.y - 100)
		trail_sprite.position = Vector2(random_x, random_y)
		trail_sprite.scale = Vector2(0.3, 0.3)  # Smaller in test mode
		print("[TEST] Art created at: ", trail_sprite.position)
	else:
		# Trail mode - use last trail position
		trail_sprite.position = last_trail_position
		trail_sprite.scale = Vector2(0.5, 0.5)
		print("[TRAIL] Art created at: ", last_trail_position)
	
	add_child(trail_sprite)
	trail_images.append(trail_sprite)
