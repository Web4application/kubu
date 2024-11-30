{
"data": {
"train_data_path": "data/train",
"test_data_path": "data/test",
"batch_size": 32,
"image_size": [150, 150]
},
"data_augmentation": {
"rotation_range": 20,
"width_shift_range": 0.2,
"height_shift_range": 0.2,
"shear_range": 0.2,
"zoom_range": 0.2,
"horizontal_flip": true,
"fill_mode": "nearest"
},
"advanced_data_augmentation": {
"mixup": {
"enabled": true,
"alpha": 0.2
},
"cutmix": {
"enabled": true,
"alpha": 1.0
}
},
"model": {
"input_shape": [150, 150, 3],
"num_classes": 2,
"dropout_rate": 0.5
},
"training": {
"epochs": 10,
"learning_rate": 0.001,
"validation_split": 0.2
},
"hyperparameter_tuning": {
"enabled": true,
"method": "grid_search",
"parameters": {
"learning_rate": [0.001, 0.01, 0.1],
"batch_size": [16, 32, 64],
"epochs": [10, 20, 30]
}
},
"distributed_training": {
"enabled": true,
"strategy": "MirroredStrategy",
"num_gpus": 2
},
"checkpoint": {
"save_best_only": true,
"save_weights_only": false,
"monitor": "val_loss",
"mode": "min",
"filepath": "checkpoints/model-{epoch:02d}-{val_loss:.2f}.h5"
},
"early_stopping": {
"monitor": "val_loss",
"patience": 10,
"mode": "min"
},
"learning_rate_scheduler": {
"schedule": "exponential_decay",
"initial_learning_rate": 0.001,
"decay_steps": 100000,
"decay_rate": 0.96,
"staircase": true
},
"optimizer": {
"type": "Adam",
"learning_rate": 0.001,
"beta_1": 0.9,
"beta_2": 0.999,
"epsilon": 1e-07
},
"advanced_regularization": {
"dropout": {
"enabled": true,
"rate": 0.5
},
"l1_l2": {
"enabled": true,
"l1": 0.01,
"l2": 0.01
}
},
"model_ensembling": {
"enabled": true,
"methods": ["bagging", "boosting"],
"num_models": 5
},
"custom_callbacks": {
"reduce_lr_on_plateau": {
"enabled": true,
"monitor": "val_loss",
"factor": 0.1,
"patience": 5,
"min_lr": 1e-6
},
"csv_logger": {
"enabled": true,
"filename": "training_log.csv"
}
},
"monitoring": {
"enabled": true,
"service": "Slack",
"webhook_url": "https://hooks.slack.com/services/your/webhook/url"
},
"data_versioning": {
"enabled": true,
"version": "1.0.0",
"storage_path": "data/versions"
},
"logging": {
"log_level": "INFO",
"log_file": "logs/training.log"
},
"data_paths": {
"validation_data_path": "data/validation",
"test_data_path": "data/test"
},
"general_ai": {
"enabled": true,
"description": "General AI settings for basic tasks",
"tasks": ["classification", "regression"]
},
"predictive_ai": {
"enabled": true,
"description": "Settings for predictive AI models",
"forecast_horizon": 10,
"features": ["feature1", "feature2", "feature3"]
},
"self_aware_ai": {
"enabled": true,
"description": "Simulated self-aware AI settings",
"reflection_interval": 5
},
"reactive_ai": {
"enabled": true,
"description": "Settings for reactive AI models",
"rules": {
"hungry": "eat",
"tired": "sleep",
"bored": "play"
}
},
"machine_learning": {
"enabled": true,
"algorithms": ["SVM", "RandomForest", "KNN"],
"parameters": {
"SVM": {
"C": [0.1, 1, 10],
"kernel": ["linear", "rbf"]
},
"RandomForest": {
"n_estimators": [100, 200, 300],
"max_depth": [10, 20, 30]
},
"KNN": {
"n_neighbors": [3, 5, 7],
"weights": ["uniform", "distance"]
}
}
}
}
