extends CharacterBody2D

@onready var sprite = $PlayerSprite

func _ready():
    create_simple_texture()

func create_simple_texture():
    var image = Image.create(32, 32, false, Image.FORMAT_RGB8)
    image.fill(Color(0.5, 0.8, 1.0))
    var texture = ImageTexture.create_from_image(image)
    sprite.texture = texture