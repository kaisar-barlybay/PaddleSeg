import os
import sys

from tools.predict import main, parse_args
from utilities.base import Base


class Runner(Base):
  def __init__(self) -> None:
    self.model_path = os.path.join(os.getcwd(), 'outputs', 'hrsegnetb48', 'best_model', 'model.pdparams')
    self.config_path = os.path.join(os.getcwd(), 'configs', 'hrsegnet', 'hrsegnetb48.yml')
    super().__init__()

  def run_model(self, image_path: str, destination_path: str):
    if not os.path.exists(destination_path):
      os.makedirs(destination_path)
    # Simulate command line arguments
    sys.argv = [
      'script.py',
      '--config',
      self.config_path,
      '--model_path',
      self.model_path,
      '--image_path',
      image_path,
      '--save_dir',
      destination_path
    ]

    # Now, when you call parse_args(), it will use the above arguments
    args = parse_args()

    # Call the main function with these arguments
    main(args)