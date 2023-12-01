## setup

- paddlepaddle: `pip install paddlepaddle-gpu`
- paddleseg:
  ```
  pip install -r requirements.txt
  pip install -v -e .
  pip install paddleseg
  ```

## Run Windows

```
python P:\PaddleSeg\tools\predict.py ^
--config P:\PaddleSeg\configs\hrsegnet\hrsegnetb48.yml ^
--model_path P:\PaddleSeg\outputs\hrsegnetb48\best_model\model.pdparams ^
--image_path Z:\datasets\cracks\crack_segmentation_dataset\images\CFD_001.jpg ^
--save_dir P:\PaddleSeg\outputs\hrsegnetb48\result
```

## build docker

- config nvidia-container: `https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt`

```
docker build -t cuda-cudnn .


docker run --gpus all -p 8888:8888 -v ./notebooks:/notebooks cuda-cudnn

```

## flask

```
flask --app main --debug run
```
