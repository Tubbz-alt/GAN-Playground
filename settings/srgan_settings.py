### Data settings ###
# Data source settings (RELATIVE TO TRAIN SCRIPT POSITION OR ABSOLUTE)
DATASET_PATH = "datasets/all_normalized__256x256"

# If none will be provided then script will select some random one
CUSTOM_HR_TEST_IMAGES = ["datasets/testing_image1.png", "datasets/testing_image2.png", "datasets/testing_image3.jpg"]

# Augmentation settings
FLIP_CHANCE = 0.30
ROTATION_CHANCE = 0.30
ROTATION_AMOUNT = 20
BLUR_CHANCE = 0.1
BLUR_AMOUNT = 0.1

# Num of worker used to preload data for training/testing
NUM_OF_LOADING_WORKERS = 12

# Num of batches preloaded in buffer
BUFFERED_BATCHES = 100

# Leave this false only when you are sure your dataset is consistent (Check whole dataset if all images have same dimensions before training)
CHECK_DATASET = False

### Training settings ###
# Episodes from training episodes
GENERATOR_PRETRAIN_EPISODES = 50_000
TRAINING_EPISODES = 400_000

BATCH_SIZE = 8

# Num of episodes after whitch progress image/s will be created to "track" progress of training
PROGRESS_IMAGE_SAVE_INTERVAL = 100
# Num of episodes after whitch weights will be saved (Its not the same as checkpoint!)
WEIGHTS_SAVE_INTERVAL = 1_000

# Base LRs
GEN_LR = 1e-4
DISC_LR = 1e-4

# Schedule of LR
GEN_LR_DECAY_INTERVAL = 40_000
GEN_LR_DECAY_FACTOR = 0.5
GEN_MIN_LR = 1e-7

DISC_LR_DECAY_INTERVAL = 40_000
DISC_LR_DECAY_FACTOR = 0.5
DISC_MIN_LR = 1e-7

# Label smoothing settings
DISC_REAL_LABEL_SMOOTHING = True
DISC_FAKE_LABEL_SMOOTHING = True
GENERATOR_LABEL_SMOOTHING = False

# Discriminator label noise settings
# Leave as None for not use noise
DISCRIMINATOR_START_NOISE = 0.1
DISCRIMINATOR_NOISE_DECAY = 0.99999
# Noise target where stop decaying
DISCRIMINATOR_TARGET_NOISE = 0.005

# Discriminator training settings
DISCRIMINATOR_TRAINING_MULTIPLIER = 1

### Model settings ###
# Number of doubling resolution
NUM_OF_UPSCALES = 2
GEN_MODEL = "mod_srgan_exp_v2"
GEN_WEIGHTS = None
DISC_MODEL = "mod_base_9layers"
DICS_WEIGHTS = None

GEN_LOSS = "mae"
DISC_LOSS = "binary_crossentropy"
FEATURE_LOSS = "mae"

FEATURE_EXTRACTOR_LAYERS = [2, 5, 8] # [2, 5, 8], [5, 9]

GEN_LOSS_WEIGHT = 1.0 # 0.8
DISC_LOSS_WEIGHT = 0.01 # 0.01, 0.003
FEATURE_PER_LAYER_LOSS_WEIGHTS = [0.025, 0.025, 0.025] # 0.0833

### General Settings ###
# Check if you want to load last autocheckpoint (If weights were provided thne checkpoint will be overriden by them)
LOAD_FROM_CHECKPOINTS = True

# Save progress images to folder too (if false then they will be saved only to tensorboard)
SAVE_RAW_IMAGES = True
# Duration of one frame if gif is created from progress images after training
GIF_FRAME_DURATION = 300