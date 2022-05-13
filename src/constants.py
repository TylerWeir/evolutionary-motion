# Environment constants
TRACK_WIDTH = 800

# Environment appearance
SCREEN_BACKGROUND_COLOR = (232, 232, 232)

# Agent Appearence
AGENT_BASE_WIDTH = 40
AGENT_BASE_HEIGHT = 20
AGENT_POLE_RADIUS = 3
HIGHLIGHT_THICKNESS = 4
HIGHLIGHT_COLOR = (255, 0, 0)
HIGHLIGHT_ALPHA = 150

# Agent Behavior
BASE_FORCE_NOISE = 0.2
ROD_ACC_NOISE = 10

# Neural Net Appearence
NODE_RADIUS = 12
NODE_VERT_SPACE = 10
LAYER_SPACE = 200

# Weight Colors
NEGATIVE_COLOR = (255, 0, 0)
MIDDLE_COLOR = (0, 0, 0)
POSITIVE_COLOR = (0, 0, 255)

# Training parameters
SUCCESS_THRESHOLD = 5_000 # >= this score indicates the net is a success and is probably stable
RANDOM_MIXIN = 0.1 # portion of agents each round to intialize fresh (not descendants of previous nets)