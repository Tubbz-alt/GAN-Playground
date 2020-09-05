import os
import sys
import traceback
import colorama
import subprocess
from colorama import Fore

colorama.init()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
stdin = sys.stdin
sys.stdin = open(os.devnull, 'w')
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
sys.stdin = stdin
sys.stderr = stderr

import tensorflow as tf
tf.get_logger().setLevel('ERROR')
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_memory_growth(gpus[0], True)
  except:
    pass

from keras.optimizers import Adam

from modules.gans import SRGAN
from modules.keras_extensions.custom_adam_optimizer import AccumulateAdam
from settings.srgan_settings import *

if __name__ == '__main__':
  training_object = None
  if not os.path.exists("training_data/srgan"): os.makedirs("training_data/srgan")
  tbmanager = subprocess.Popen("./venv/Scripts/python.exe -m tensorboard.main --logdir training_data/srgan --samples_per_plugin=images=200 --port 6006", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  try:
    training_object = SRGAN(DATASET_PATH, num_of_upscales=NUM_OF_UPSCALES, training_progress_save_path="training_data/srgan",
                            batch_size=BATCH_SIZE, buffered_batches=BUFFERED_BATCHES,
                            gen_mod_name=GEN_MODEL, disc_mod_name=DISC_MODEL,
                            generator_optimizer=Adam(GEN_LR, 0.9), discriminator_optimizer=Adam(DISC_LR, 0.9),
                            generator_lr_decay_interval=GEN_LR_DECAY_INTERVAL, discriminator_lr_decay_interval=DISC_LR_DECAY_INTERVAL,
                            generator_lr_decay_factor=GEN_LR_DECAY_FACTOR, discriminator_lr_decay_factor=DISC_LR_DECAY_FACTOR,
                            generator_min_lr=GEN_MIN_LR, discriminator_min_lr=DISC_MIN_LR,
                            discriminator_label_noise=DISCRIMINATOR_START_NOISE, discriminator_label_noise_decay=DISCRIMINATOR_NOISE_DECAY, discriminator_label_noise_min=DISCRIMINATOR_TARGET_NOISE,
                            generator_weights=GEN_WEIGHTS, discriminator_weights=DICS_WEIGHTS,
                            load_from_checkpoint=LOAD_FROM_CHECKPOINTS,
                            custom_hr_test_images_paths=CUSTOM_HR_TEST_IMAGES, check_dataset=CHECK_DATASET, num_of_loading_workers=NUM_OF_LOADING_WORKERS)

    training_object.save_models_structure_images()

    training_object.train(TRAINING_EPISODES, pretrain_episodes=GENERATOR_PRETRAIN_EPISODES,
                          discriminator_training_multiplier=DISCRIMINATOR_TRAINING_MULTIPLIER,
                          progress_images_save_interval=PROGRESS_IMAGE_SAVE_INTERVAL, save_raw_progress_images=SAVE_RAW_IMAGES,
                          weights_save_interval=WEIGHTS_SAVE_INTERVAL,
                          discriminator_smooth_real_labels=True, discriminator_smooth_fake_labels=True,
                          generator_smooth_labels=False)
  except KeyboardInterrupt:
    if training_object:
      print(Fore.BLUE + f"Quiting on epoch: {training_object.episode_counter} - This could take little time, get some coffe and rest :)" + Fore.RESET)
  except Exception as e:
    if training_object:
      print(Fore.RED + f"Exception on epoch: {training_object.episode_counter}" + Fore.RESET)
    else:
      print(Fore.RED + "Creating training object failed" + Fore.RESET)
    traceback.print_exc()
  finally:
    if training_object:
      training_object.save_checkpoint()

  if training_object:
    if input("Create gif of progress? ") == "y": training_object.make_progress_gif(frame_duration=GIF_FRAME_DURATION)

  try:
    tbmanager.send_signal(subprocess.signal.CTRL_C_EVENT)
    tbmanager.wait()
  except:
    pass