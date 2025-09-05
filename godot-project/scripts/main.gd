extends Node2D

@onready var http = HTTPRequest.new()
@onready var sprite = $Sprite2D

func _ready():
    add_child(http)
    http.request_completed.connect(_on_art_received)
    
    # Test AI generation
    generate_test_art()

func generate_test_art():
    var json_data = JSON.stringify({"prompt": "pixel art test sprite", "seed": 42})
    var headers = ["Content-Type: application/json"]
    http.request("http://localhost:8081/generate", headers, HTTPClient.METHOD_POST, json_data)

func _on_art_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
    if response_code == 200:
        var json = JSON.new()
        if json.parse(body.get_string_from_utf8()) == OK:
            var data = json.data
            if data.success:
                var image_data = Marshalls.base64_to_raw(data.image)
                var image = Image.new()
                image.load_png_from_buffer(image_data)
                var texture = ImageTexture.create_from_image(image)
                sprite.texture = texture
                print("✓ AI art loaded!")

func _input(event):
    if event is InputEventKey and event.pressed and event.keycode == KEY_SPACE:
        generate_test_art()