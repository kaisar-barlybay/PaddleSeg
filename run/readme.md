## setup

- paddlepaddle: `pip install paddlepaddle-gpu`
- paddleseg:
  ```
  pip install -r requirements.txt
  pip install -v -e .
  pip install paddleseg
  ```
- check installation: `import paddle; paddle.utils.run_check()`

## Run Windows

#### !

```
python P:\PaddleSeg\tools\predict.py ^
--config P:\PaddleSeg\configs\hrsegnet\hrsegnetb48.yml ^
--model_path P:\PaddleSeg\outputs\hrsegnetb48_custom\best_model\model.pdparams ^
--image_path Z:\datasets\cracks\Заколы\фото\04.10.2023\converted ^
--save_dir Z:\datasets\cracks\Заколы\фото\04.10.2023\predicted
```

## Train Windows

### from scratch

```
python P:\PaddleSeg\tools\train.py ^
--config P:\PaddleSeg\configs\hrsegnet\hrsegnetb48.yml ^
--do_eval ^
--use_vdl ^
--save_interval 500 ^
--save_dir P:\PaddleSeg\outputs\hrsegnetb48_custom
```

### continue

```
python P:\PaddleSeg\tools\train.py ^
--config P:\PaddleSeg\configs\hrsegnet\hrsegnetb48.yml ^
--resume_model P:\PaddleSeg\outputs\hrsegnetb48\iter_100000 ^
--do_eval ^
--use_vdl ^
--save_interval 1000 ^
--save_dir P:\PaddleSeg\outputs\hrsegnetb48_custom
```

## visualize

### windows

```
visualdl ^
--logdir P:\PaddleSeg\outputs\hrsegnetb48_custom ^
--model P:\PaddleSeg\outputs\hrsegnetb48_custom\best_model\model.pdparams ^
--host localhost ^
--port 8002 ^
--cache-timeout <cache_timeout> ^
--language <language> ^
--public-path <public_path> ^
--api-only --component_tabs <tab_name1, tab_name2, ...> ^
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
