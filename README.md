### Project Structure (Simplified)

[Website](https://r-iot.ufrn.br/)

```
├── conda_environment.txt
├── config.yaml
├── dataset/
│   ├── pose_estimation/
│   └── segmentation/
├── models/
│   ├── LLMs/
│   └── yolo_train_infer/
│       ├── pose_estimation/
│       ├── segmentation/
│       └── tracking/
├── pipelines/
├── tests/
├── utils/
├── pyproject.toml
├── README.md
```

### Folder Descriptions

* `dataset/`: Datasets for segmentation and pose estimation tasks.
* `models/`: Training and inference files for various models.
* `pipelines/`: Processing pipelines and orchestration scripts.
* `tests/`: Unit and integration tests.
* `utils/`: Utility functions and helper scripts.
* `config.yaml`: Main configuration file.
* `conda_environment.txt`: Conda environment specification.
* `pyproject.toml`: Project metadata and build configuration.

